"""Collect Constitutional Court (MK) decisions from www.mkri.id.

Two steps, both polite (one request every few seconds, named user agent):

    python mk_crawl.py list   --out ../tables/mk_decisions.csv
    python mk_crawl.py pdfs   --csv ../tables/mk_decisions.csv --dir <private folder> [--limit N]

`list` reads the public decision list (www.mkri.id/perkara/persidangan/putusan,
100 per page) and writes one row per decision. The page is a Next.js app: the
records sit in the React Server Components payload embedded in the HTML
(`self.__next_f.push(...)`), long strings stored as separate `T` chunks and
referenced as "$<id>". This script decodes that payload; it calls no API.

`pdfs` downloads each decision's PDF from s.mkri.id/public/content/... (allowed
by s.mkri.id/robots.txt) and skips files already present, so it can resume.
PDFs stay out of git, like the licensed exports in ../../review.

Standard library only. Python 3.9+.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

LIST_URL = "https://www.mkri.id/perkara/persidangan/putusan?page={page}&perPage={per}"
USER_AGENT = "imrdata-research-crawler/0.1 (+https://github.com/pranotoiskandar-collab/imrdata)"
FIELDS = [
    "putusancode", "jenisnya", "no_perkara", "date", "status", "pokok_perkara",
    "pemohon", "keywords", "amar_putusan", "supporting_file",
]
PUSH = re.compile(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)')
TOTAL = re.compile(r"of\s+([0-9][0-9.,]*)")


def fetch(url, retries=3):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code in (403, 429):  # blocked or rate-limited: stop, do not retry
                sys.exit(f"stopped: HTTP {error.code} on {url}")
            if attempt == retries - 1:
                raise
            time.sleep(30 * (attempt + 1))
        except Exception as error:  # network hiccup: back off and retry
            if attempt == retries - 1:
                raise
            print(f"  retry after {error}", file=sys.stderr)
            time.sleep(30 * (attempt + 1))


def flight_payload(html):
    """Join the RSC payload pieces embedded in a Next.js page."""
    return "".join(json.loads(m.group(1)) for m in PUSH.finditer(html))


def flight_rows(flight):
    """Split the payload into rows: id -> raw text.

    A row is either 'id:<json>\\n' or 'id:T<hex byte length>,<text>' with no
    terminator, so text rows are cut by byte length and the next row follows
    directly.
    """
    data = flight.encode("utf-8")
    rows, pos = {}, 0
    while pos < len(data):
        colon = data.find(b":", pos)
        if colon < 0:
            break
        row_id = data[pos:colon].decode("ascii", errors="ignore").strip()
        if data[colon + 1:colon + 2] == b"T":
            comma = data.find(b",", colon)
            size = int(data[colon + 2:comma], 16)
            rows[row_id] = data[comma + 1:comma + 1 + size].decode("utf-8", errors="ignore")
            pos = comma + 1 + size
        else:
            end = data.find(b"\n", colon)
            end = len(data) if end < 0 else end
            rows[row_id] = data[colon + 1:end].decode("utf-8", errors="ignore")
            pos = end + 1
    return rows


def items_array(rows):
    """Return the parsed {"items": [...]} object of the decision list."""
    flight = next(text for text in rows.values() if '{"items":[' in text)
    start = flight.index('{"items":[')
    depth, in_string, escaped = 0, False, False
    for end in range(start, len(flight)):
        char = flight[end]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(flight[start:end + 1])
    raise ValueError("items array not closed")


def resolve(value, chunks):
    if isinstance(value, str) and re.fullmatch(r"\$[0-9a-f]+", value):
        return chunks.get(value[1:], value)
    return value


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def parse_list_page(html):
    chunks = flight_rows(flight_payload(html))
    rows = []
    for item in items_array(chunks)["items"]:
        rows.append({field: clean(resolve(item.get(field), chunks)) for field in FIELDS})
    total = TOTAL.search(re.sub(r"<[^>]+>", " ", html))
    return rows, total


def crawl_list(out, per, delay):
    rows, page, total = [], 1, None
    while True:
        html = fetch(LIST_URL.format(page=page, per=per)).decode("utf-8")
        page_rows, _ = parse_list_page(html)
        if not page_rows:
            break
        rows.extend(page_rows)
        print(f"page {page}: {len(page_rows)} rows, {len(rows)} so far", file=sys.stderr)
        page += 1
        time.sleep(delay)
    seen, unique = set(), []
    for row in rows:
        if row["putusancode"] not in seen:
            seen.add(row["putusancode"])
            unique.append(row)
    write_csv(out, unique)
    print(f"wrote {len(unique)} decisions to {out}", file=sys.stderr)


def write_csv(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def download_pdfs(csv_path, folder, limit, delay):
    os.makedirs(folder, exist_ok=True)
    with open(csv_path, encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["supporting_file"].startswith("https://s.mkri.id/public/")]
    fetched = 0
    for row in rows:
        target = os.path.join(folder, f"mk_{row['putusancode']}.pdf")
        if os.path.exists(target) and os.path.getsize(target) > 0:
            continue
        if limit and fetched >= limit:
            break
        data = fetch(row["supporting_file"])
        with open(target, "wb") as handle:
            handle.write(data)
        fetched += 1
        print(f"{row['no_perkara']}: {len(data):,} bytes", file=sys.stderr)
        time.sleep(delay)
    print(f"downloaded {fetched} PDFs into {folder}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="write the decision list as CSV")
    listing.add_argument("--out", default="../tables/mk_decisions.csv")
    listing.add_argument("--per", type=int, default=100)
    listing.add_argument("--delay", type=float, default=5.0, help="seconds between requests")
    pdfs = sub.add_parser("pdfs", help="download decision PDFs listed in the CSV")
    pdfs.add_argument("--csv", default="../tables/mk_decisions.csv")
    pdfs.add_argument("--dir", required=True, help="folder outside git for the PDFs")
    pdfs.add_argument("--limit", type=int, default=0, help="stop after N new files (0 = all)")
    pdfs.add_argument("--delay", type=float, default=5.0, help="seconds between requests")
    args = parser.parse_args()
    if args.command == "list":
        crawl_list(args.out, args.per, args.delay)
    else:
        download_pdfs(args.csv, args.dir, args.limit, args.delay)


if __name__ == "__main__":
    main()

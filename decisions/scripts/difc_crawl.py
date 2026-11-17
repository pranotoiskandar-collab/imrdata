"""Collect DIFC Courts judgments and orders from www.difccourts.ae.

Two steps, both polite (one request every few seconds, named user agent):

    python difc_crawl.py list  --out ../tables/difc_judgments.csv
    python difc_crawl.py texts --csv ../tables/difc_judgments.csv --out ../tables/difc_texts.jsonl

`list` pages through the public listing (www.difccourts.ae/rules-decisions/
judgments-orders, 12 items a page, newest first) and writes one row per
judgment or order. The sitemap is not used: it stops in early 2021.

`texts` opens each judgment page and stores its full text (the page holds the
whole judgment as HTML; there is no PDF). It writes JSON lines and skips URLs
already in the output, so it can resume.

robots.txt allows these paths (it disallows only /menu and /videos).
Standard library only. Python 3.9+.
"""

import argparse
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

BASE = "https://www.difccourts.ae"
LIST_URL = BASE + "/rules-decisions/judgments-orders?ccm_paging_p={page}&ccm_order_by=ak_date&ccm_order_by_direction=desc"
USER_AGENT = "imrdata-research-crawler/0.1 (+https://github.com/pranotoiskandar-collab/imrdata)"
FIELDS = ["case_no", "title", "date", "court", "label", "url"]
MONTHS = {m: i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}

ITEM = re.compile(
    r'<div class="each_result content_set">\s*<h4><a href="([^"]+)">(.*?)</a></h4>\s*'
    r'<p class="label_small">(.*?)</p>', re.S)
DETAIL = re.compile(r'<div class="content_set_detail[^"]*">\s*<div class="content_desc">(.*?)<div class="push">', re.S)
HEADING = re.compile(r'<div class="div_outer">\s*<h4>(.*?)</h4>', re.S)
CASE_NO = re.compile(r"\b(SCT|CFI|CA|ARB|ENF|TCD|DEC|JJC)[\s/-]*(\d{3,4})\s*[/-]\s*(\d{4})")
CITATION = re.compile(r"\[(\d{4})\]\s*(?:DIFC\s+)?(SCT|CFI|CA|ARB|ENF|TCD|DEC|JJC)\s+(\d{3,4})")
# The court comes from the URL folder; the site's own label is a loose tag list.
COURTS = {
    "small-claims-tribunal": "Small Claims Tribunal", "court-first-instance": "Court of First Instance",
    "court-appeal": "Court of Appeal", "arbitration": "Arbitration", "enforcement": "Enforcement",
    "technology-and-construction-division": "Technology and Construction Division",
    "joint-judicial-committee": "Joint Judicial Committee",
    "court-administrative-orders": "Court Administrative Orders", "digital-economy-court": "Digital Economy Court",
}


def fetch(url, retries=3):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as error:
            if error.code in (403, 429):  # blocked or rate-limited: stop, do not retry
                sys.exit(f"stopped: HTTP {error.code} on {url}")
            if error.code == 404 or attempt == retries - 1:
                raise
            time.sleep(30 * (attempt + 1))
        except Exception as error:  # network hiccup: back off and retry
            if attempt == retries - 1:
                raise
            print(f"  retry after {error}", file=sys.stderr)
            time.sleep(30 * (attempt + 1))


def text_of(fragment):
    """HTML fragment to plain text, keeping paragraph breaks."""
    fragment = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", fragment)
    fragment = re.sub(r"(?i)<br\s*/?>|</(p|div|h\d|li|tr)>", "\n", fragment)
    fragment = html.unescape(re.sub(r"<[^>]+>", "", fragment))
    lines = [re.sub(r"[ \t\xa0]+", " ", line).strip() for line in fragment.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def iso_date(text):
    match = re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})", text)
    if not match or match.group(1).capitalize() not in MONTHS:
        return ""
    return f"{match.group(3)}-{MONTHS[match.group(1).capitalize()]:02d}-{int(match.group(2)):02d}"


def split_label(label):
    """'November 06, 2026  Court of First Instance - Orders' -> ISO date, rest of the label."""
    label = re.sub(r"\s+", " ", html.unescape(label)).strip()
    match = re.match(r"([A-Za-z]+ \d{1,2}, \d{4}) ?(.*)", label)
    return (iso_date(match.group(1)), match.group(2)) if match else ("", label)


def case_number(text):
    """'CFI 024/2026', 'ARB/031/2025' or '[2025] SCT 946' -> 'CFI 024/2026' form."""
    case = CASE_NO.search(text)
    if case:
        return f"{case.group(1)} {case.group(2)}/{case.group(3)}"
    cite = CITATION.search(text)
    return f"{cite.group(2)} {cite.group(3)}/{cite.group(1)}" if cite else ""


def row_from(url, title, label):
    url = html.unescape(url)
    title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", title))).strip()
    date, label = split_label(label)
    folder = url.split("/judgments-orders/")[-1].split("/")[0]
    return {"case_no": case_number(title), "title": title, "date": date,
            "court": COURTS.get(folder, folder), "label": label, "url": url}


def crawl_list(out, delay, max_pages):
    rows, seen = [], set()
    for page in range(1, max_pages + 1):
        items = ITEM.findall(fetch(LIST_URL.format(page=page)))
        if not items:
            break
        for url, title, label in items:
            if url not in seen:
                seen.add(url)
                rows.append(row_from(url, title, label))
        print(f"page {page}: {len(items)} items, {len(rows)} so far", file=sys.stderr)
        time.sleep(delay)
    write_csv(out, rows)
    print(f"wrote {len(rows)} judgments and orders to {out}", file=sys.stderr)


def crawl_texts(csv_path, out, delay, limit):
    with open(csv_path, encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    done = set()
    if os.path.exists(out):
        with open(out, encoding="utf-8") as handle:
            done = {json.loads(line)["url"] for line in handle if line.strip()}
    fetched = 0
    with open(out, "a", encoding="utf-8") as handle:
        for row in rows:
            if row["url"] in done:
                continue
            if limit and fetched >= limit:
                break
            page = fetch(row["url"])
            body = DETAIL.search(page)
            heading = HEADING.search(page)
            text = text_of(body.group(1)) if body else ""
            handle.write(json.dumps({"url": row["url"], "title": text_of(heading.group(1)) if heading else "",
                                     "text": text},
                                    ensure_ascii=False) + "\n")
            fetched += 1
            print(f"{row['title'][:70]}: {len(text):,} chars", file=sys.stderr)
            time.sleep(delay)
    print(f"added {fetched} texts to {out}", file=sys.stderr)


def write_csv(path, rows):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="write the judgment list as CSV")
    listing.add_argument("--out", default="../tables/difc_judgments.csv")
    listing.add_argument("--delay", type=float, default=5.0, help="seconds between requests")
    listing.add_argument("--max-pages", type=int, default=2000)
    texts = sub.add_parser("texts", help="fetch the full text of each judgment")
    texts.add_argument("--csv", default="../tables/difc_judgments.csv")
    texts.add_argument("--out", default="../tables/difc_texts.jsonl")
    texts.add_argument("--limit", type=int, default=0, help="stop after N new texts (0 = all)")
    texts.add_argument("--delay", type=float, default=5.0, help="seconds between requests")
    args = parser.parse_args()
    if args.command == "list":
        crawl_list(args.out, args.delay, args.max_pages)
    else:
        crawl_texts(args.csv, args.out, args.delay, args.limit)


if __name__ == "__main__":
    main()

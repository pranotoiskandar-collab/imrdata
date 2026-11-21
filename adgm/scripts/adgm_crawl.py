"""Collect ADGM Courts (Abu Dhabi) judgments from www.adgm.com.

Three steps, all polite (one request every few seconds, named user agent):

    python adgm_crawl.py list  --out ../tables/adgm_judgments.csv
    python adgm_crawl.py pdfs  --csv ../tables/adgm_judgments.csv --dir <private folder>
    python adgm_crawl.py texts --csv ../tables/adgm_judgments.csv --dir <private folder> --out ../tables/adgm_texts.jsonl

`list` pages through www.adgm.com/adgm-courts/judgments?page=N (10 rows a
page, newest first) until a page is empty. Each row is one case; a judgment
that decides several cases appears once per case, sharing one PDF.

`pdfs` downloads each judgment PDF from assets.adgm.com and skips files already
present. `texts` runs `pdftotext -layout` (poppler) on each PDF.

robots.txt allows /adgm-courts/ (it disallows /api/, /episerver, /util and a
few site sections). Standard library only, plus the pdftotext command.
"""

import argparse
import csv
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

LIST_URL = "https://www.adgm.com/adgm-courts/judgments?page={page}"
USER_AGENT = "imrdata-research-crawler/0.1 (+https://github.com/pranotoiskandar-collab/imrdata)"
FIELDS = ["citation", "court", "case_no", "name", "date", "pdf_url", "pdf_file"]
ROW = re.compile(r"<adgm-table-row>(.*?)</adgm-table-row>", re.S)
CELL = re.compile(r'<adgm-table-cell id="(\w+)">(.*?)</adgm-table-cell>', re.S)
LINK = re.compile(r'<a href="(https://assets\.adgm\.com/[^"]+)"[^>]*>(.*?)</a>', re.S)
CITATION = re.compile(r"\[(\d{4})\]\s*(ADGM[A-Z]+)\s*0*(\d+)")


def fetch(url, retries=3):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read()
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


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text))).strip()


def norm_citation(text):
    match = CITATION.search(text)
    return f"[{match.group(1)}] {match.group(2)} {int(match.group(3)):03d}" if match else clean(text)


def pdf_name(url):
    return hashlib.sha1(url.encode()).hexdigest()[:12] + ".pdf"


def parse_list_page(page):
    rows = []
    for block in ROW.findall(page):
        cells = {key: clean(value) for key, value in CELL.findall(block)}
        try:
            date = datetime.strptime(cells.get("date", ""), "%d %b %Y").date().isoformat()
        except ValueError:
            date = ""
        for url, label in LINK.findall(block):
            citation = norm_citation(label)
            rows.append({"citation": citation, "court": "Court of Appeal" if "ADGMCA" in citation else "Court of First Instance",
                         "case_no": cells.get("caseNumber", ""), "name": cells.get("caseName", ""), "date": date,
                         "pdf_url": html.unescape(url), "pdf_file": pdf_name(html.unescape(url))})
    return rows


def crawl_list(out, delay, max_pages):
    rows, seen = [], set()
    for number in range(1, max_pages + 1):
        page_rows = parse_list_page(fetch(LIST_URL.format(page=number)).decode("utf-8", errors="replace"))
        if not page_rows:
            break
        for row in page_rows:
            key = (row["case_no"], row["pdf_url"])
            if key not in seen:
                seen.add(key)
                rows.append(row)
        print(f"page {number}: {len(page_rows)} rows, {len(rows)} so far", file=sys.stderr)
        time.sleep(delay)
    write_csv(out, rows)
    print(f"wrote {len(rows)} rows to {out}", file=sys.stderr)


def read_csv(path):
    with open(path, encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def download_pdfs(csv_path, folder, delay):
    os.makedirs(folder, exist_ok=True)
    done = 0
    for url in dict.fromkeys(row["pdf_url"] for row in read_csv(csv_path)):
        target = os.path.join(folder, pdf_name(url))
        if os.path.exists(target) and os.path.getsize(target) > 0:
            continue
        with open(target, "wb") as handle:
            handle.write(fetch(url))
        done += 1
        print(f"{done}: {target}", file=sys.stderr)
        time.sleep(delay)
    print(f"downloaded {done} PDFs into {folder}", file=sys.stderr)


def extract_texts(csv_path, folder, out):
    rows = read_csv(csv_path)
    by_pdf = {}
    for row in rows:
        by_pdf.setdefault(row["pdf_url"], []).append(row)
    with open(out, "w", encoding="utf-8") as handle:
        for url, group in by_pdf.items():
            path = os.path.join(folder, pdf_name(url))
            text = ""
            if os.path.exists(path):
                text = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
            first = group[0]
            handle.write(json.dumps({"citation": first["citation"], "court": first["court"], "date": first["date"],
                                     "case_nos": [row["case_no"] for row in group],
                                     "names": [row["name"] for row in group], "pdf_url": url, "text": text},
                                    ensure_ascii=False) + "\n")
    print(f"wrote {len(by_pdf)} texts to {out}", file=sys.stderr)


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
    listing.add_argument("--out", default="../tables/adgm_judgments.csv")
    listing.add_argument("--delay", type=float, default=5.0)
    listing.add_argument("--max-pages", type=int, default=500)
    pdfs = sub.add_parser("pdfs", help="download the judgment PDFs")
    pdfs.add_argument("--csv", default="../tables/adgm_judgments.csv")
    pdfs.add_argument("--dir", required=True, help="folder outside git for the PDFs")
    pdfs.add_argument("--delay", type=float, default=5.0)
    texts = sub.add_parser("texts", help="extract text from the PDFs with pdftotext")
    texts.add_argument("--csv", default="../tables/adgm_judgments.csv")
    texts.add_argument("--dir", required=True)
    texts.add_argument("--out", default="../tables/adgm_texts.jsonl")
    args = parser.parse_args()
    if args.command == "list":
        crawl_list(args.out, args.delay, args.max_pages)
    elif args.command == "pdfs":
        download_pdfs(args.csv, args.dir, args.delay)
    else:
        extract_texts(args.csv, args.dir, args.out)


if __name__ == "__main__":
    main()

# DIFC Courts judgments and orders

Dubai International Financial Centre Courts, kept apart from the Indonesian corpus in `../decisions`.

Collected 17 Nov 2026 from www.difccourts.ae/rules-decisions/judgments-orders: **5,151 judgments and orders**, the site's full count, dated 2007 to 6 Nov 2026. Court of First Instance 3,729 · Small Claims Tribunal 770 · Court of Appeal 251 · Arbitration 158 · Technology and Construction Division 139 · Enforcement 60 · Court Administrative Orders 30 · Digital Economy Court 14. The XML sitemap stops in early 2021 (2,236 links), so the listing pages were used instead.

- `tables/difc_judgments.csv`: one row per item: `case_no` (e.g. `CFI 024/2026`, normalised from the title, a `[2025] DIFC SCT 946` citation or the "Claim No." line), `title`, `date` (ISO), `court` (from the URL folder), `label` (the site's own tag, e.g. "Court of First Instance - Orders"; it is inconsistent across years), `url`, `chars` (length of the text). 51 rows have no case number (administrative orders and odd titles); 4 have no usable date on the site; 3 pages are empty on the site.
- `tables/difc_texts.jsonl.gz`: the full English text of each item, one JSON object per line (`url`, `case_no`, `title`, `date`, `court`, `text`), about 59 million characters. Read with `gzip.open(path, "rt")`.

**How it was collected.** The cloud machine cannot reach difccourts.ae, so the listing and pages were read in the Claude desktop app's browser on a Mac in Dubai, one request every 3 to 5 seconds, using the same parsing as `scripts/difc_crawl.py`. Paging by date skips items that share a date, so the listing was read twice (by date and by name) and merged; the union matches the site's total. robots.txt allows these paths. DIFC judgments are published for public use, so the texts are kept in git, unlike the MK PDFs in `../decisions`.

```
cd difc/scripts
python3 difc_crawl.py list  --out ../tables/difc_judgments.csv      # ~430 requests, 5 s apart
python3 difc_crawl.py texts --csv ../tables/difc_judgments.csv --out ../tables/difc_texts.jsonl --limit 20
```

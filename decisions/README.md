# Court decisions: international norms in judicial reasoning

Corpus of court decisions, collected to study how domestic legal reasoning takes up (or leaves out) international norms. Indonesia first; the DIFC Courts (Dubai) are added as an English-language comparison.

## Sources

| Source | Status | Script |
|---|---|---|
| Constitutional Court (MK), www.mkri.id | open; crawled first | `scripts/mk_crawl.py` |
| Supreme Court Direktori Putusan (putusan3.mahkamahagung.go.id) | blocked (403) outside Indonesia; robots.txt disallows by default; access to be requested from the MA | none yet |
| SIPP (court dockets) | captcha or bot challenge on most courts; dockets only, no reasoning | not planned |
| DIFC Courts (Dubai), www.difccourts.ae | open; full English text in HTML | `scripts/difc_crawl.py` |

Assessment of every repository (17 Nov 2026): https://claude.ai/artifact/K9pRJRVL4ryuzh2yzN2wuv

## MK decisions

`tables/mk_decisions.csv` was collected on 17 Nov 2026: **5,207 decisions** (the site listed 5,208; one moved between pages during collection), 2003-11-14 to 2026-11-12. PUU 2,608 · PHPKADA 1,570 · PHPU 998 · SKLN 31. Every row has a PDF link; one row has an empty `amar_putusan`, and a few PHPU rows carry very long rulings (up to ~300,000 characters), so raise Python's `csv.field_size_limit` when reading it.

**How it was collected.** www.mkri.id answers scripted clients with HTTP 403 (tested once from a Mac with this script's user agent; the script stops on 403/429 and does not retry). The list was therefore read in the Claude desktop app's browser, one page of 100 every 10 seconds, with the same parsing logic as `scripts/mk_crawl.py`. The script is kept for when MK grants access (a request for a bulk export was drafted the same day).

```
cd decisions/scripts
python3 mk_crawl.py list --out ../tables/mk_decisions.csv          # ~53 requests, 5 s apart
python3 mk_crawl.py pdfs --csv ../tables/mk_decisions.csv --dir ~/imrdata-private/mk_pdf --limit 20
```

- `tables/mk_decisions.csv`: one row per decision: `putusancode` (MK's id), `jenisnya` (PUU, SKLN, PHPU, PHPKADA), `no_perkara`, `date`, `status` (type of ruling), `pokok_perkara`, `pemohon`, `keywords`, `amar_putusan`, `supporting_file` (PDF URL).
- PDFs are public but large (about 0.4 MB each, ~2 GB in all), so they stay outside git, in the private folder, as with the Scopus exports in `../review`.
- The crawler identifies itself, waits 5 seconds between requests, and only reads paths that robots.txt allows. It reads the public list pages, not any internal API.

## DIFC Courts judgments and orders

Collected 17 Nov 2026 from www.difccourts.ae/rules-decisions/judgments-orders: **5,151 judgments and orders**, the site's full count, dated 2007 to 6 Nov 2026. Court of First Instance 3,729 · Small Claims Tribunal 770 · Court of Appeal 251 · Arbitration 158 · Technology and Construction Division 139 · Enforcement 60 · Court Administrative Orders 30 · Digital Economy Court 14. The XML sitemap stops in early 2021 (2,236 links), so the listing pages were used instead.

- `tables/difc_judgments.csv`: one row per item: `case_no` (e.g. `CFI 024/2026`, normalised from the title, a `[2025] DIFC SCT 946` citation or the "Claim No." line), `title`, `date` (ISO), `court` (from the URL folder), `label` (the site's own tag, e.g. "Court of First Instance - Orders"; it is inconsistent across years), `url`, `chars` (length of the text). 51 rows have no case number (administrative orders and odd titles); 4 have no usable date on the site; 3 pages are empty on the site.
- `tables/difc_texts.jsonl.gz`: the full English text of each item, one JSON object per line (`url`, `case_no`, `title`, `date`, `court`, `text`), about 59 million characters. Read with `gzip.open(path, "rt")`.

**How it was collected.** The cloud machine cannot reach difccourts.ae, so the listing and pages were read in the Claude desktop app's browser on a Mac in Dubai, one request every 3 to 5 seconds, using the same parsing as `scripts/difc_crawl.py`. Paging by date skips items that share a date, so the listing was read twice (by date and by name) and merged; the union matches the site's total. robots.txt allows these paths. DIFC judgments are published for public use, so the texts are kept in git, unlike the MK PDFs.

```
cd decisions/scripts
python3 difc_crawl.py list  --out ../tables/difc_judgments.csv      # ~430 requests, 5 s apart
python3 difc_crawl.py texts --csv ../tables/difc_judgments.csv --out ../tables/difc_texts.jsonl --limit 20
```

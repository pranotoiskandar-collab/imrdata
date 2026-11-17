# Court decisions: international norms in Indonesian judicial reasoning

Corpus of Indonesian court decisions, collected to study how domestic legal reasoning takes up (or leaves out) international norms.

## Sources

| Source | Status | Script |
|---|---|---|
| Constitutional Court (MK), www.mkri.id | open; crawled first | `scripts/mk_crawl.py` |
| Supreme Court Direktori Putusan (putusan3.mahkamahagung.go.id) | blocked (403) outside Indonesia; robots.txt disallows by default; access to be requested from the MA | none yet |
| SIPP (court dockets) | captcha or bot challenge on most courts; dockets only, no reasoning | not planned |

Assessment of every repository (17 Nov 2026): https://claude.ai/artifact/K9pRJRVL4ryuzh2yzN2wuv

## MK decisions

```
cd decisions/scripts
python3 mk_crawl.py list --out ../tables/mk_decisions.csv          # ~53 requests, 5 s apart
python3 mk_crawl.py pdfs --csv ../tables/mk_decisions.csv --dir ~/imrdata-private/mk_pdf --limit 20
```

- `tables/mk_decisions.csv`: one row per decision: `putusancode` (MK's id), `jenisnya` (PUU, SKLN, PHPU, PHPKADA), `no_perkara`, `date`, `status` (type of ruling), `pokok_perkara`, `pemohon`, `keywords`, `amar_putusan`, `supporting_file` (PDF URL).
- PDFs are public but large (about 0.4 MB each, ~2 GB in all), so they stay outside git, in the private folder, as with the Scopus exports in `../review`.
- The crawler identifies itself, waits 5 seconds between requests, and only reads paths that robots.txt allows. It reads the public list pages, not any internal API.

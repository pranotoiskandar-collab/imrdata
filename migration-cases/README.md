# Migration cases: Gulf States and East Asia

Court decisions on migration (immigration, refugees and non-refoulement, migrant workers, deportation, nationality, trafficking) from the GCC states and East Asia. Collected to feed IMR's [Court Decisions database](https://theimr.org/court-decisions/) and the farmworker view of the [Migration Law Atlas](https://theimr.org/migration-law/?lens=farm) (Global Farmworker Law).

Started 17 Nov 2026. Work in progress.

## Files

- `keywords.json`: search terms per jurisdiction in the court's own languages. `migration` terms find candidates; `farm` terms flag farm, livestock and fishing cases for the farmworker view.
- `tables/candidates.csv`: every search hit before reading, one row per case: `jurisdiction`, `source`, `court`, `case_no`, `date`, `title`, `url`, `lang`, `matched_terms`, `farm_terms`, `retrieved`.
- `tables/decisions.csv`: cases that have been read and coded, in the same columns as IMR's `decisions.csv` (`id` … `sources`), so rows can be moved into the database as they are. New rows start with `status` S until checked against the judgment.
- `scripts/kr_lawgo.py`: Korean precedents and Constitutional Court decisions from the law.go.kr Open API (needs a free key).

## Sources

Checked 17 Nov 2026 (robots.txt and terms).

| Jurisdiction | Source | How |
|---|---|---|
| South Korea | law.go.kr public search (robots.txt allows all): precedents and Constitutional Court | browser, slow; `scripts/kr_lawgo.py` if an API key is obtained later |
| Japan | courts.go.jp judgment search | browser, slow |
| Hong Kong | HKLII (robots.txt disallows only `/api`) | browser, slow |
| Taiwan | Judicial Yuan open-data bulk files (bots disallowed; manual download) | filter after download |
| Macau | court.gov.mo | browser, slow |
| Mongolia | shuukh.mn | browser, slow |
| UAE | DIFC Courts (from the DIFC crawl), ADGM Courts | browser |
| Qatar | QICDRC (crawl-delay 10 s); Al Meezan (terms to check) | browser |
| Saudi Arabia | MOJ and Board of Grievances published volumes (PDF) | manual |
| Bahrain, Kuwait, Oman | no public judgment database | printed collections or requests |
| China | China Judgements Online requires login and forbids scraping | not crawled; SPC typical cases by hand |

The cloud sessions behind this repository cannot reach these sites, so collection runs in the Claude app's browser on a personal computer, one page at a time with pauses, as with the MK and DIFC collections. Crawlers identify themselves as `imrdata-research-crawler` and read only what robots.txt allows. Full judgment texts stay outside git, as with the MK PDFs.

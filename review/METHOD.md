# Global dialogue in legal scholarship, seen from Indonesia: method and data for review

Prepared 15 November 2026 for an independent check of the data and methods behind the dashboard's interpretations. The dashboard itself: https://claude.ai/artifact/WQXUK9ZNBrL2caD8aKte8d

**What we ask of the reviewer.** Check whether each claim below follows from the data and computation listed for it, and flag any step where the method could produce the result by itself, or where a different reasonable choice would change the conclusion. The interpretations are the authors'. This note is only about whether the numbers support them.

## 1. Data sources

| # | Source | What it contains | Coverage | Where |
|---|---|---|---|---|
| D1 | SCImago Journal Rank 2025, category Law (3308) | The 87 Indonesian journals, quartile, SJR | 2025 edition | `tables/journals.csv` |
| D2 | Scopus "citing documents" export, per journal | One row per document citing the journal in its latest CiteScore window (4 years) | 85 of 87 journals; 21,972 rows | raw exports: private folder (licensed) |
| D3 | Scopus document export with references | The 7,046 documents the 87 journals published in 2022–2025 and their ~290,000 references | 2022–2025 | raw: private folder |
| D4 | Scopus source list, October 2026 | Publisher, subject codes (ASJC) and source type of every indexed title | | public from Elsevier |
| D5 | SCImago Law rankings by country | Number of law journals and quartiles per country | 72 countries; UK pending | `tables/countries.csv` |
| D6 | Journal websites | Editorial-board lists (70 journals); abstracts via Crossref (2,963 English); full-text headings (89) | 2022–2025 | `tables/boards.csv`, `tables/template.csv` |
| D7 | Web of Science Core Collection, all editions | Searches listed in `tables/wos_counts.csv` | counted 15 Nov 2026 | `tables/wos_counts.csv` |
| D9 | Journal fee pages (DOAJ as fallback) | Author fee of each journal | read 15 Nov 2026 | `tables/apc_journals.csv` |
| D8 | Regulations and decrees | Published texts, quoted | 2005–2026 | `tables/regs.csv` |

## 2. Core definitions

- **Citing row**: one document in D2 that cites a listed journal. **Reference**: one item in a reference list in D3.
- **Received (in the list)** for journal A: rows in A's export whose source is another listed journal. **Given**: times A appears as the citing source in the other journals' exports. Self-citations are excluded from both. **Net** = received − given.
- **Venue group** (Indonesian / Global South / Northern publisher / unclear): assigned from the citing source's title, DOI prefix and Scopus record. Unresolved venues stay "unclear" and are not guessed.
- **Publisher class**: title matched to D4. "Western university press" = Oxford, Cambridge, Chicago, Johns Hopkins, Duke, Edinburgh, Toronto, MIT and similar; "major Western commercial" = Elsevier, Springer, Wiley, Taylor & Francis, SAGE, Emerald, Brill, De Gruyter.

## 3. Claims, and what supports each

| Dashboard section | Claim | Data | Computation | Please check |
|---|---|---|---|---|
| Indonesia among the world's law journals | 87 law journals, 22 in Q1; apart from the US, UK and Netherlands, no country checked has more | D5 | counts per country | UK still missing; SCImago assigns journals to the publisher's country |
| Where the citations come from | about 85% of citing rows come from Indonesian venues (18,638 of 21,972) | D2 | venue group shares of 21,972 rows | venue classification (`scripts/gs.py`) |
| What the listed journals cite | ~113,000 references point to periodicals outside Indonesia | D3 | references parsed and matched by title | reference parsing is approximate; about a quarter cannot be placed (`scripts/refs.py`) |
| Western university presses (one-way street) | cited 6,868 times by the journals, cite them back 14 times; commercial 37,885 vs 527 | D2, D3, D4 | both directions matched to D4 | title matching between D3 strings and D4 (`scripts/press.py`) |
| Net receivers and givers | some journals take in far more than they give | D2 | received − given per journal | self-citation exclusion; 85-journal scope (`tables/balance.csv`, `scripts/recip.py`) |
| Is the share from abroad growing? | no; same 43 journals: 16.4% → 13.5% (2023–2025) | D2 by CiteScore year | fixed panel of journals | panel choice (`tables/trend.csv`) |
| Shared editors and citations | pairs sharing 3+ board members exchange more citations | D2, D6 | pairs grouped by shared members; mean citations per pair | name matching across boards; correlation, not cause (`scripts/boards_data.py`) |
| In what language are the cited works? | share of English references rising | D3 | language guessed from common words | word-list classifier (`tables/lang.csv`) |
| Do the articles follow a template? | 83% of abstracts state a method vs 32% in university-press journals; 23% aim-method-results in order vs 1% | D6 | regular-expression patterns on both sets alike | pattern lists and sampling (`scripts/measures.py`, `scripts/sel.py`); 199 comparison abstracts only |
| Web of Science: coverage | only 2 of 87 journals in WoS, both ESCI | D7 | ISSN search | ISSN completeness; title check run as a control |
| Web of Science: Indonesia entering | Indonesian-author law records 88 (2022) → 201 (2025) | D7 | CU=Indonesia AND WC=Law by year | category Law only; author address, not journal country |
| Conference papers and books | Scopus: 2.0% of citing documents are conference papers, ~1.4% books; WoS Indonesian law output: 16% conference, 9% books | D2, D4, D7 | source type from D4 + conference lists + DOI patterns (`scripts/inc.py`) | ~113 unmatched items counted as books |
| What Web of Science does not see | for 7 Scopus-only journals, Scopus records 6,036 citing documents, WoS 538 | D2, D7 | WoS cited-reference search on journal names | name variants; different time windows (Scopus 4-year window vs WoS cited years 2018–2026) |
| Who pays to publish | 51 of 87 journals charge authors (median Rp 5m); 2025 fees ≈ Rp 7–9 bn | D1, D9 | fee × 2025 documents per journal; low = domestic rate, unknown = 0; high = foreign rate, unknown = median (`scripts/est.py`) | waivers and extras not modelled; fee pages sometimes contradict themselves |

## 4. Known limits we would most like checked

1. **Venue and reference matching by title.** Most classifications rest on string matching (normalised titles, DOI prefixes). Errors are likely small but not measured.
2. **Two time frames.** Incoming citations use each journal's CiteScore window; outgoing references cover 2022–2025.
3. **Scope.** 85 of 87 journals for citation measures (one has no export; one is outside the open-access scope).
4. **Classifiers by rule.** Language and template features are detected by word patterns, not read by hand.
5. **Inference vs. description.** The dashboard describes distributions. Statements of reason (e.g. why journals chose Scopus) are marked as plausible readings, not tested.

## 5. Files

- `tables/`: every table the dashboard draws from (aggregates only).
- `scripts/`: the Python scripts that produced them. Paths inside point to the authors' working folders; the raw exports they read are licensed (Scopus, Web of Science) and are shared privately on request, not in this public package.

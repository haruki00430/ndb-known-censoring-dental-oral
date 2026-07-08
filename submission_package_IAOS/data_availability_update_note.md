# Data Availability Statement — Update Note

## Current text in v0.8 manuscript (Declarations section)

> The source NDB Open Data files and population denominator sources are publicly available from the Japan Ministry of Health, Labour and Welfare and the Statistics Bureau of Japan. Derived analysis files and code can be made available by the authors, subject to repository or journal requirements.

## Updated text to insert before submission (after GitHub/Zenodo are live)

Replace the current Data availability statement with:

```
The NDB Open Data files used in this analysis are publicly available from the Japan 
Ministry of Health, Labour and Welfare (https://www.mhlw.go.jp/stf/seisakunitsuite/
bunya/0000177182.html). Population denominator data are publicly available from the 
Statistics Bureau of Japan (https://www.stat.go.jp/english/data/jinsui/). All 
analysis code and derived non-suppressed output files are openly available on GitHub 
(https://github.com/haruki00430/ndb-known-censoring-dental-oral) and permanently 
archived on Zenodo (https://doi.org/10.5281/zenodo.[ZENODO_DOI]).
```

## Action items

- [ ] Create GitHub repository: `haruki00430/ndb-known-censoring-dental-oral`
- [ ] Push code to GitHub and make repository public
- [ ] Create Zenodo release and obtain DOI
- [ ] Replace `[ZENODO_DOI]` with actual DOI in the DOCX manuscript
- [ ] Update `Known_Censoring_Not_Missingness_integrated_draft_v0_8.docx` Declarations section

## What to upload to GitHub

| Path | Content |
|------|---------|
| `scripts/full_extraction.py` | Full dental/oral cell extraction |
| `scripts/qc_and_tables.py` | QC + table generation |
| `scripts/step1_build_population_inventory.py` | Population denominator build |
| `scripts/steps2_8_rate_bounds_demo.py` | Rate bounds and ranking demo |
| `scripts/generate_figure4_final_v2.py` | Figure generation (v2, English) |
| `figure_data/figure4_rate_bounds_ranking_demo.csv` | Figure source data |
| `results/rate_bounds_demo/` | Rate bounds and ranking outputs |
| `outputs/figure4_rate_bounds_ranking_demo_final_v2.png` | Final figure (v2) |
| `manuscript_tables/` | Table 1-4 in CSV + MD format |
| `README.md` | Repository README (bilingual) |
| `CITATION.cff` | Citation metadata |
| `LICENSE` | CC BY 4.0 |
| `REPRODUCE.md` | Reproduction instructions |

## What NOT to upload

- `02_Data/raw/` (NDB raw data — license prohibits redistribution)
- `submission_package_IAOS/` (manuscript files — managed separately)
- `.claude/`, `.obsidian/` (AI tool settings)

# Known Censoring, Not Missingness: Cell Suppression and Partial Identification in Open Administrative Healthcare Data

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.PLACEHOLDER.svg)](https://doi.org/10.5281/zenodo.PLACEHOLDER)

## Overview

This repository contains the analysis code and derived output files for the paper:

> Haruki Saito, Tetsuya Ohira. Known Censoring, Not Missingness: Cell Suppression and Partial Identification in Open Administrative Healthcare Data. *Statistical Journal of the IAOS* (under review, 2026).

We evaluate whether cell suppression in Japan's NDB (National Database) Open Data can be treated as an interval-censoring and partial-identification problem rather than generic missing data. Using prefecture-level Dental/Oral disease-count files from releases No.1–No.11 (fiscal years 2014–2024), we:

1. Verify release-specific disclosure rules and classify suppressed cells by subtype
2. Assign `[1, 9]` count bounds only to verified primary low-count cells
3. Demonstrate how known censoring affects rate bounds and prefecture ranking support

---

## 概要（日本語）

本リポジトリは以下の論文の解析コードおよび派生出力ファイルを公開しています。

> [著者名]. Known Censoring, Not Missingness: Cell Suppression and Partial Identification in Open Administrative Healthcare Data. *Statistical Journal of the IAOS*（審査中, 2026）

厚生労働省「NDBオープンデータ」の歯科・口腔疾患数ファイル（No.1–No.11、FY2014–FY2024）を用い、セル抑制を欠損値ではなく区間打ち切りおよび部分識別問題として扱う手法を示します。

---

## Repository Structure

```
├── scripts/
│   ├── full_extraction.py               # Step 2: Full cell extraction (311 indicators × 10 releases)
│   ├── qc_and_tables.py                 # Step 3: QC + manuscript tables (Table 1–4)
│   ├── step1_build_population_inventory.py  # Step 4a: Population denominator construction
│   ├── steps2_8_rate_bounds_demo.py     # Step 4b: Rate bounds and ranking demo
│   └── generate_figure4_final_v2.py     # Step 5: Figure generation (English, 300 dpi)
├── figure_data/
│   └── figure4_rate_bounds_ranking_demo.csv  # Figure source data (2,068 rows)
├── results/
│   └── rate_bounds_demo/
│       ├── population_denominator_inventory.csv  # 470 prefecture-year rows
│       ├── demo_count_bounds.csv         # 1,410 cells × count bounds
│       ├── demo_rate_bounds.csv          # 1,410 cells × rate bounds
│       ├── demo_ranking_stability.csv    # 1,410 cells × ranking status
│       └── demo_naive_ranking_comparison.csv  # 5,640 rows (naive strategies)
├── manuscript_tables/
│   ├── table1_release_rule_inventory.csv
│   ├── table2_observability_by_release.csv
│   ├── table3_suppression_subtype_bounds.csv
│   └── table4_naive_handling_strategies.csv
├── outputs/
│   └── figure4_rate_bounds_ranking_demo_final_v2.png  # Final figure (300 dpi)
├── CITATION.cff
├── LICENSE
└── REPRODUCE.md
```

---

## Data Sources

| Data | Source | Notes |
|------|--------|-------|
| NDB Open Data (Dental/Oral) | [Ministry of Health, Labour and Welfare](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html) | Releases No.1–No.11; **raw files not redistributed** |
| Population denominators (FY2014) | [e-Stat table 0003104195](https://www.e-stat.go.jp/) | Population Census basis H22/H26 |
| Population denominators (FY2015–2019) | [e-Stat table 0003459027](https://www.e-stat.go.jp/) | Population Census basis H27 |
| Population denominators (FY2020, 2022–2024) | [Statistics Bureau estimates](https://www.stat.go.jp/english/data/jinsui/) | Population estimate R2 basis |

**Note**: NDB Open Data raw files are publicly available from MHLW but are not redistributed here. Download them directly from the MHLW website and place under `02_Data/raw/NDB_OpenData/` before running the scripts.

---

## Key Findings

- **71,017 prefecture-level cells** retained across 10 releases (No.8/FY2021 excluded: metric change)
- **36.2% overall suppression rate** — varies from 18.1% (No.11) to 46.9% (No.1)
- **Only 19.4% of suppressed cells** (4,982/25,732) were eligible for `[1, 9]` count bounds
- In a 3-indicator rate demonstration (1,410 cells): 700 point-identified, 92 bounded, 618 ambiguous
- **Verified disclosure rules do not automatically imply numeric identifiability**

---

## Requirements

```
Python >= 3.9
pandas >= 2.0
numpy >= 1.24
matplotlib >= 3.7
geopandas >= 0.13      # For figure generation
scipy >= 1.11
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Reproduction

See [REPRODUCE.md](REPRODUCE.md) for full step-by-step instructions.

```bash
# Step 1: Build population denominator inventory
python scripts/step1_build_population_inventory.py

# Step 2–4: Full cell extraction
python scripts/full_extraction.py

# Step 5: QC and table generation
python scripts/qc_and_tables.py

# Step 6: Rate bounds and ranking demo
python scripts/steps2_8_rate_bounds_demo.py

# Step 7: Generate figure
python scripts/generate_figure4_final_v2.py
```

---

## Citation

If you use this code or data in your research, please cite:

```
Haruki Saito, Tetsuya Ohira. Known Censoring, Not Missingness: Cell Suppression and 
Partial Identification in Open Administrative Healthcare Data. 
Statistical Journal of the IAOS (under review, 2026).
```

Or see [CITATION.cff](CITATION.cff) for machine-readable citation metadata.

---

## License

This repository is licensed under [CC BY 4.0](LICENSE).  
You are free to share and adapt the materials provided that appropriate credit is given.

---

## Contact

Haruki Saito  
Department of Epidemiology, Fukushima Medical University School of Medicine  
Fukushima, Japan  
Email: [haruki.saito@fmu.ac.jp — confirm before submission]  
ORCID: [0009-0009-7890-6068](https://orcid.org/0009-0009-7890-6068)

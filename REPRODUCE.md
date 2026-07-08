# Reproduction Instructions

This document describes how to reproduce all results from:

> Known Censoring, Not Missingness: Cell Suppression and Partial Identification in Open Administrative Healthcare Data

## Environment

Tested on Python 3.11, Windows 11. Should also work on macOS/Linux.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### requirements.txt (minimum)

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
scipy>=1.11
geopandas>=0.13
openpyxl>=3.1
japanize-matplotlib>=1.1   # Japanese font support for figure generation
```

---

## Data Download

Raw NDB Open Data are NOT included in this repository. Download them from:

> Ministry of Health, Labour and Welfare: https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html

Place the downloaded files under:

```
02_Data/raw/NDB_OpenData/
```

The analysis requires Dental/Oral disease-count files from releases No.1–No.11
(fiscal years 2014–2024). The exact subdirectory structure mirrors the MHLW
release archive.

Population denominator data (publicly available):

- FY2014: e-Stat table 0003104195
- FY2015–2019: e-Stat table 0003459027
- FY2020, 2022–2024: Statistics Bureau population estimate files

Place population CSV files under:

```
02_Data/raw/Statistics_Bureau/
```

---

## Analysis Steps (Run in Order)

### Step 1 — Build population denominator inventory

```bash
python scripts/step1_build_population_inventory.py
```

**Output**: `results/rate_bounds_demo/population_denominator_inventory.csv`  
Expected: 470 rows (47 prefectures × 10 retained fiscal years)

### Step 2 — Full dental/oral cell extraction

```bash
python scripts/full_extraction.py
```

**Output** (`results/full_extraction/`):
- `dental_file_inventory.csv`
- `dental_rule_inventory.csv`
- `dental_indicator_catalog.csv` (311 indicators)
- `dental_cell_state_full.csv` (71,017 cells)
- `dental_bounds_primary.csv` (4,982 primary-bounded cells)

**Expected cell counts** (cross-check):
- Total cells: 71,017
- Observed: 45,285
- Suppressed: 25,732
- Primary low-count (No.3–No.4 only): 4,982
- Ambiguous: 20,750

### Step 3 — QC and manuscript table generation

```bash
python scripts/qc_and_tables.py
```

**Output** (`manuscript_tables/`):
- `table1_release_rule_inventory.csv` / `.md`
- `table2_observability_by_release.csv` / `.md`
- `table3_suppression_subtype_bounds.csv` / `.md`
- `table4_naive_handling_strategies.csv` / `.md`

Also produces QC report at `qc/dental_full_extraction_qc_report.md`.

### Step 4 — Rate bounds and ranking demonstration

```bash
python scripts/steps2_8_rate_bounds_demo.py
```

**Output** (`results/rate_bounds_demo/`):
- `demo_indicator_selection.csv` (3 indicators)
- `demo_count_bounds.csv` (1,410 rows)
- `demo_rate_bounds.csv` (1,410 rows)
- `demo_ranking_stability.csv` (1,410 rows)
- `demo_naive_ranking_comparison.csv` (5,640 rows)

Also produces `figure_data/figure4_rate_bounds_ranking_demo.csv` (2,068 rows, 3 panels).

**Expected demo results**:
- Point identified: 700 cells (49.6%)
- Bounded primary: 92 cells (6.5%)
- Not bounded (ambiguous): 618 cells (43.8%)
- Stable ranks: 472 cells
- Rank intervals: 320 cells
- Ranking not supported: 618 cells

### Step 5 — Generate Figure 1 (main figure)

```bash
python scripts/generate_figure4_final_v2.py
```

**Output** (`outputs/`):
- `figure4_rate_bounds_ranking_demo_final_v2.png` (300 dpi)
- `figure4_rate_bounds_ranking_demo_final_v2.svg`

---

## Verification

After running all steps, verify these key outputs match expected values:

| File | Expected |
|------|----------|
| `dental_cell_state_full.csv` | 71,017 rows |
| `dental_bounds_primary.csv` | 4,982 rows |
| `population_denominator_inventory.csv` | 470 rows |
| `demo_rate_bounds.csv` | 1,410 rows |
| `figure4_rate_bounds_ranking_demo.csv` | 2,068 rows |

---

## Random Seed

No stochastic processes are used in this analysis. All results are deterministic.

---

## Exclusion Note

- Release No.8 (FY2021) is excluded in all scripts because the metric changed from
  disease count to claim/calculation count. This is coded in `full_extraction.py`
  as `EXCLUDED_RELEASES = ['No.8']`.

- The `[1, 9]` count bounds are assigned ONLY to cells from No.3–No.4 under
  verified aggressive-rule row-context logic. Standard-rule releases (No.5–No.11)
  are conservatively classified as ambiguous.

---

## Contact

For questions about the analysis code, contact:  
[CORRESPONDING_AUTHOR_NAME] — [EMAIL]

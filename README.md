[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21257142.svg)](https://doi.org/10.5281/zenodo.21257142)

> **Repository (GitHub):** https://github.com/haruki00430/ndb-known-censoring-dental-oral  
> **Zenodo DOI:** https://doi.org/10.5281/zenodo.21257142  
> **Reproduction:** [`REPRODUCE.md`](REPRODUCE.md) · [`CITATION.cff`](CITATION.cff)

# Known Censoring, Not Missingness: Cell Suppression and Partial Identification in Open Administrative Healthcare Data

**論文タイトル（日本語）**: 欠損ではなく既知の打ち切り——公開行政医療データにおけるセル抑制と部分識別

**Manuscript status**: Submitted to *Statistical Journal of the IAOS* (Sage) — 2026-07-08  
**Repository:** https://github.com/haruki00430/ndb-known-censoring-dental-oral

---

## Abstract / 研究概要

Open administrative healthcare datasets suppress small cells for confidentiality, but suppressed values are often analyzed as missing, zero, or imputed counts. We evaluated whether suppression in prefecture-level Dental/Oral files from Japan's NDB Open Data could instead be treated as a known-censoring and partial-identification problem. We inventoried releases No.1 through No.11, verified disclosure rules, classified cells, assigned [1, 9] count bounds only to verified primary low-count suppression, and used population denominators to evaluate rate bounds and ranking support.

Ten disease-count releases were retained; release No.8 was excluded because the metric changed from disease count to claim/calculation count. The retained data contained 311 distinct Dental/Oral indicator labels, 1,511 release-indicator rows, and 71,017 prefecture-level cells. Of these cells, 45,285 were observed and 25,732 were suppressed. Among suppressed cells, 4,982 were primary low-count cells assigned [1, 9] bounds, whereas 20,750 were ambiguous and were not assigned bounds. Ranking support was stable for 472 cells, interval-ranked for 320 cells, and not supported for 618 ambiguous cells.

---

公開行政医療データでは，小セルが機密保護のために抑制されているが，抑制された値はしばしば欠損値，ゼロ，または補完値として扱われている。本研究は，日本の NDB オープンデータの都道府県レベル歯科傷病数ファイルにおける抑制を，既知の打ち切り（known-censoring）および部分識別問題として扱えるかを評価した。No.1〜No.11 の全リリースを調査し，開示ルールを検証してセルを分類し，確認済み一次低カウント抑制のみに [1, 9] カウント境界を割り当て，人口分母を用いてレート境界と順位支持性を評価した。

10 リリースの傷病数データを保持（No.8 は指標変更のため除外）。311 の歯科指標ラベル，71,017 セルのうち，45,285 は観測済み，25,732 は抑制済みであった。抑制セルのうち，4,982 セルに [1, 9] 境界を割り当て，20,750 セルは境界付与不可な「曖昧抑制」に分類された。

---

## Submission / 投稿情報

| Item | Content |
|------|---------|
| Journal | [*Statistical Journal of the IAOS*](https://journals.sagepub.com/home/sji) (Sage) |
| Article type | Research Article |
| Submitted | 2026-07-08 |
| Status | Under review |

---

## Repository Structure / ディレクトリ構造

```
ndb-known-censoring-dental-oral/
├── README.md                           # This file / 本ファイル
├── CITATION.cff                        # Citation metadata / 引用メタデータ
├── REPRODUCE.md                        # Reproduction instructions / 再現手順
├── LICENSE                             # CC BY 4.0
├── scripts/
│   ├── full_extraction.py              # Step 2: Full cell extraction / セル全抽出
│   ├── qc_and_tables.py                # Step 3: QC + manuscript tables / QC + 論文テーブル
│   ├── step1_build_population_inventory.py  # Step 4a: Population denominators / 人口分母構築
│   ├── steps2_8_rate_bounds_demo.py    # Step 4b: Rate bounds & ranking / レート境界・順位
│   └── generate_figure4_final_v2.py   # Step 5: Figure generation / 図生成
├── figure_data/
│   ├── figure4_rate_bounds_ranking_demo.csv  # Figure source data (2,068 rows) / 図データ
│   ├── figure1_rule_variant_timeline.csv     # Rule variant timeline / 開示ルール変遷
│   ├── figure2_observability_heatmap_data.csv
│   └── figure3_bounds_eligibility_by_release.csv
├── results/
│   └── rate_bounds_demo/
│       ├── population_denominator_inventory.csv  # 470 prefecture-year rows
│       ├── demo_count_bounds.csv         # 1,410 cells × count bounds
│       ├── demo_rate_bounds.csv          # 1,410 cells × rate bounds per 100,000
│       ├── demo_ranking_stability.csv    # 1,410 cells × ranking status
│       └── demo_naive_ranking_comparison.csv  # 5,640 rows (4 naive strategies)
├── manuscript_tables/
│   ├── table1_release_rule_inventory.{csv,md}   # Table 1 / 論文テーブル 1
│   ├── table2_observability_by_release.{csv,md} # Table 2 / 論文テーブル 2
│   ├── table3_suppression_subtype_bounds.{csv,md} # Table 3
│   └── table4_naive_handling_strategies.{csv,md}  # Table 4
├── outputs/
│   ├── figure4_rate_bounds_ranking_demo_final_v2.png  # Main figure (300 dpi)
│   ├── figure4_rate_bounds_ranking_demo_final_v2.svg
│   └── figure4_rate_bounds_ranking_demo_final_caption.md
├── submission_package_IAOS/
│   ├── Known_Censoring_Not_Missingness_integrated_draft_v0_8.md   # Manuscript (MD)
│   ├── Known_Censoring_Not_Missingness_integrated_draft_v0_8.docx # Manuscript (DOCX)
│   ├── Known_Censoring_Not_Missingness_supplement_v0_8.md         # Supplement (MD)
│   ├── Known_Censoring_Not_Missingness_supplement_v0_8.docx       # Supplement (DOCX)
│   └── v0_8_submission_final/
│       ├── figure1_rate_bounds_ranking_support_main.png
│       └── supplementary_figure_s1_naive_ranking.png
├── qc/
│   ├── dental_full_extraction_qc_report.md
│   └── dental_full_extraction_qc_summary.json
└── docs/
    ├── Dental_Oral_Full_Extraction_Report_20260707.md
    ├── Dental_Oral_QC_Table_Generation_Report_20260707.md
    ├── Dental_Oral_Rate_Bounds_Ranking_Demo_Report_20260707.md
    └── Dental_Oral_Figure4_Final_Generation_Report_20260708.md
```

---

## Key Findings / 主な発見

| Finding / 発見 | Description / 内容 |
|---------------|-------------------|
| **Cell inventory** | 71,017 prefecture-level cells across 10 retained releases / 保持 10 リリースで 71,017 セル |
| **Suppression rate** | 36.2% overall; 47% (No.1/FY2014) → 18% (No.11/FY2024) / 全体 36.2%；リリースにより 18–47% |
| **Bounds eligibility** | Only 19.4% of suppressed cells eligible for [1,9] bounds / 抑制セルの 19.4% のみ境界付与可 |
| **Aggressive rule** | No.3–4 allow partial identification via row context / No.3–4 は行コンテキストで一次識別可 |
| **Standard rule** | No.5–11 suppressed cells conservatively ambiguous / No.5–11 は保守的に「曖昧抑制」分類 |
| **Ranking support** | 472/1,410 demo cells: stable point rank; 618/1,410: ranking not supported / 安定順位 472、順位不支持 618 |

---

## Cell-State Vocabulary / セル状態の用語

Suppressed cells are **never** treated as zero or imputed.  
抑制セルはゼロ扱い・補完は行わない。

| State / 状態 | Meaning / 意味 |
|-------------|---------------|
| `observed` | Numeric value present / 数値あり |
| `primary_low_count` | Hidden count in [1,9] under verified rule / 検証済みルール下で [1,9] 境界付与 |
| `ambiguous_suppression` | Cannot distinguish primary from complementary / 一次・補完を区別不可 |

---

## Data Sources / データソース

| Data / データ | Source / ソース | Notes / 備考 |
|-------------|----------------|-------------|
| NDB Open Data (Dental/Oral) | [MHLW](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html) | No.1–No.11; raw files not redistributed / 生ファイル非配布 |
| Population (FY2014) | [e-Stat 0003104195](https://www.e-stat.go.jp/) | H22/H26 Census basis |
| Population (FY2015–2019) | [e-Stat 0003459027](https://www.e-stat.go.jp/) | H27 Census basis |
| Population (FY2020, 2022–2024) | [Statistics Bureau](https://www.stat.go.jp/english/data/jinsui/) | R2 estimate basis |

**Note / 注意**: NDB Open Data raw files are publicly available from MHLW but are **not redistributed** here. Download directly from MHLW and place under `02_Data/raw/NDB_OpenData/` (two levels above this repository root) before running scripts.

---

## How to Cite / 引用方法

```
Saito H, Ohira T. Known Censoring, Not Missingness: Cell Suppression
and Partial Identification in Open Administrative Healthcare Data.
Statistical Journal of the IAOS. 2026. [Under review]
```

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

---

## Requirements / 動作環境

```
Python >= 3.9
pandas >= 2.0
numpy >= 1.24
matplotlib >= 3.7
scipy >= 1.11
geopandas >= 0.13    # for figure generation
openpyxl >= 3.1
requests >= 2.28     # for e-Stat API (step1 only)
```

See [`REPRODUCE.md`](REPRODUCE.md) for full setup and execution instructions.

---

## License / ライセンス

Code: [CC BY 4.0](LICENSE)  
Derived data: Derived from publicly available NDB Open Data. Source data are subject to the terms of the Ministry of Health, Labour and Welfare, Japan.

コード：CC BY 4.0 ライセンス。派生データは NDB オープンデータを加工したもので，厚生労働省の利用規約に従う。

---

## Contact / 連絡先

Haruki Saito  
Department of Epidemiology, Fukushima Medical University School of Medicine  
Fukushima, Japan  
ORCID: [0009-0009-7890-6068](https://orcid.org/0009-0009-7890-6068)

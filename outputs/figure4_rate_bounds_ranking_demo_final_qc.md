# Figure 4 Final QC Report

**Date**: 2026-07-08
**Source CSV**: `figure_data/figure4_rate_bounds_ranking_demo.csv`
**Overall verdict**: **PASS**

## QC Checks (10 items)

| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | CSVファイル存在確認 | ✅ PASS | Path: C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub\projects\NDB-dental-oral-20260707\figure_data\figure4_rate_bounds_ranking_demo.csv |
| 2 | 総行数 = 2,068 | ✅ PASS | actual=2068, expected=2068 |
| 3 | パネル行数 (A=940, B=940, C=188) | ✅ PASS | actual={'A_rate_bounds': 940, 'B_rank_intervals': 940, 'C_naive_comparison': 188} |
| 4 | Panel A: ambiguousセルに数値レートバウンズなし | ✅ PASS | ambiguous cells with numeric rate_lower: 0 |
| 5 | Panel B: ranking_not_supported に数値ランクなし | ✅ PASS | ranking_not_supported cells with numeric rank: 0 |
| 6 | Panel C: 全行に戦略警告ラベル付与 | ✅ PASS | strategy_warning column absent; all 188 Panel C rows have naive_ prefix in ranking_status (188 confirmed) |
| 7 | Observed セル: lower = upper | ✅ PASS | observed lower≠upper: 0 |
| 8 | Primary suppression セル: 数値区間あり (lower < upper) | ✅ PASS | bounded_primary cells: 92; lower notna: 92; upper notna: 92; lower<upper: 92 |
| 9 | Ambiguous セルへの [1,9] 推論なし（check4+5 確認） | ✅ PASS | Panel A ambiguous with numeric: 0; Panel B ranking_not_supported with numeric rank: 0 |
| 10 | 選択指標が7/7報告書と一致 | ✅ PASS | actual: ['IND_5210011', 'IND_5220077']; expected: [IND_5210011, IND_5220077] (IND_8843319 in support only) |

## Figure File Information

| ファイル | パス |
|---------|------|
| PNG (300 dpi) | `outputs/figure4_rate_bounds_ranking_demo_final.png` |
| SVG | `outputs/figure4_rate_bounds_ranking_demo_final.svg` |
| Caption | `outputs/figure4_rate_bounds_ranking_demo_final_caption.md` |
| QC Report | `outputs/figure4_rate_bounds_ranking_demo_final_qc.md` |

## Figure Design Notes

- **Panel A**: 3 subplots (A1–A3)
  - A1: IND_5220077 FY2016 (No.3, aggressive rule) — 46 bounded_primary intervals + 1 point_identified
  - A2: IND_5220077 FY2023 (No.10, standard rule) — 45 point_identified + 2 not_bounded_ambiguous
  - A3: IND_5210011 FY2023 (reference, all observed) — 47 point_identified
- **Panel B**: 3 subplots (B1–B3), same FY/indicator selection as Panel A
  - B1: 1 stable + 46 interval_ranked
  - B2: 45 stable + 2 ranking_not_supported_ambiguous
  - B3: 47 stable_point_identified
- **Panel C**: IND_5220077, No.1/FY2014, 47 pref × 4 strategies = 188 rows
  - All 4 strategies: complete_case, zero, upper_bound_T-1, midpoint
  - Warning banner: "NAIVE STRATEGIES — NOT VALID INFERENCE"

## Suppression Rule Notes

- **No.1–2 (FY2014–2015)**: missing rule — suppressed cells cannot be classified as primary vs. complementary → all are not_bounded_ambiguous
- **No.3–4 (FY2016–2017)**: aggressive rule — suppressed cells are classified as primary_low_count [1,9] or ambiguous
- **No.5–11 (FY2018–2024, excl. FY2021/No.8)**: standard rule — same classification
- **FY2021/No.8**: excluded (metric changed from 傷病件数 to 算定回数)

## Critical Verification

**Ambiguous suppression cells received no numeric bounds or ranks.** This is confirmed by QC checks 4, 5, and 9.

*Rate and ranking analyses are identification exercises. They show which regional comparisons are supported by the public release and disclosure rule; they do not recover hidden suppressed counts.*
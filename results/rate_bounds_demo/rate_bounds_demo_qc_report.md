# Rate Bounds Demo QC Report

**生成日**: 2026-07-07

**最終判定**: `RATE_RANKING_DEMO_READY`

---

## QC チェック結果

| # | チェック | 判定 | 詳細 |
|---|---------|------|------|
| 1 | Population denominator has 470 rows | ✅ PASS | actual=470; expected=470 |
| 2 | Population joins without missing prefecture-year pairs | ✅ PASS | actual_missing=0 |
| 3 | No ambiguous cell receives [1,9] count bounds | ✅ PASS | ambiguous_with_bounds_count=0 |
| 4 | No ambiguous cell receives a numeric rate bound | ✅ PASS | ambiguous_with_rate_bounds_count=0 |
| 5 | Observed cells have equal lower and upper count/rate | ✅ PASS | mismatch_count=0 |
| 6 | Primary low-count cells have count bounds [1,9] | ✅ PASS | wrong_bounds_count=0; primary_bounded_cells_total=92 |
| 7 | Naive ranking outputs are clearly labeled as comparison benchmarks | ✅ PASS |  |
| 8 | Figure 4 data exist and are consistent with rate/ranking files | ✅ PASS | rows=2068; panels=3 |

---

## 選択指標

| indicator_id   | indicator_name     | selection_role       |   retained_releases_available |   observed_cells |   primary_bounded_cells |   ambiguous_suppression_cells | selection_reason                                    |
|:---------------|:-------------------|:---------------------|------------------------------:|-----------------:|------------------------:|------------------------------:|:----------------------------------------------------|
| IND_5220077    | 血行性歯髄炎       | bounded_demo         |                            10 |              143 |                      92 |                           235 | 最多 primary_bounded_cells (92件)、observed >= 40件 |
| IND_5210011    | 根充済み           | stable_observed_demo |                            10 |              470 |                       0 |                             0 | 観測率 100.0%・ambiguous ゼロ                       |
| IND_8843319    | 限局型若年性歯周炎 | ambiguous_limit_demo |                            10 |               87 |                       0 |                           383 | ambiguous_suppression 383件でランキング不可の例示   |

## 人口分母ソース

                                              source_name                   fiscal_years  n_rows
e-Stat 人口推計 R2国勢調査基準 (Statistics Bureau pop_2023_est.csv)       [2020, 2022, 2023, 2024]     188
             e-Stat 人口推計 table_0003104195 (H22/H26国勢調査基準)                         [2014]      47
                 e-Stat 人口推計 table_0003459027 (H27国勢調査基準) [2015, 2016, 2017, 2018, 2019]     235

## 重要注記

- Rate および ranking 解析は partial identification の演習である。
- 公開リリースと開示規則によって支持される地域比較のみを示す。
- 隠れたカウントを推定・補完したものではない。
- ambiguous suppression セルはいかなる数値境界も受け取っていない。

# Rate Bounds / Ranking Demo Handoff for Codex

**生成日**: 2026-07-07
**判定**: `RATE_RANKING_DEMO_READY`

---

## 概要

Rate and ranking analyses are identification exercises. They show which regional comparisons are supported by the public release and disclosure rule, not recovered hidden counts.

---

## 人口分母

- 470行（10年 × 47都道府県）
- FY2021は除外（No.8 指標変更のため）
- FY2014: e-Stat 0003104195 直接取得（H22基準, 単位=人）
- FY2015–2019: e-Stat 0003459027 直接取得（H27基準, 単位=千人→×1000）
- FY2020,2022–2024: pop_2023_est.csv（R2基準, 単位=千人→×1000）

## 選択指標（3種）

### 1. bounded_demo: `IND_5220077` 血行性歯髄炎
- observed: 143, primary_bounded: 92, ambiguous: 235

### 2. stable_observed_demo: `IND_5210011` 根充済み
- observed: 470, primary_bounded: 0, ambiguous: 0

### 3. ambiguous_limit_demo: `IND_8843319` 限局型若年性歯周炎
- observed: 87, primary_bounded: 0, ambiguous: 383

## Rate Bounds 結果

- point_identified（観測セル）: 700
- bounded_primary（[1,9]境界）: 92
- not_bounded_ambiguous（レート境界なし）: 618

## Ranking 結果

- stable_point_identified: 472
- interval_ranked: 320
- ranking_not_supported_ambiguous: 618

## 何が推論できて何ができないか

**推論可能**:
- observed セルの点レート（完全識別）
- primary_low_count セルのレート区間 [1/pop×100k, 9/pop×100k]
- primary_bounded セルを含む指標の区間ランキング

**推論不可**:
- ambiguous suppression セルのカウントは境界不明
- ambiguous セルを含む指標の完全ランキングは成立しない
- Naive代入（zero/upper_bound_T-1/midpoint）は比較ベンチマークであり有効推論ではない

## 出力ファイル

- `population_denominator_inventory.csv` ← population_denominator_inventory
- `demo_indicator_selection.csv` ← demo_indicator_selection
- `demo_count_bounds.csv` ← demo_count_bounds
- `demo_rate_bounds.csv` ← demo_rate_bounds
- `demo_ranking_stability.csv` ← demo_ranking_stability
- `demo_naive_ranking_comparison.csv` ← demo_naive_ranking_comparison
- `figure4_rate_bounds_ranking_demo.csv` ← figure4_rate_bounds_ranking_demo
- `rate_bounds_demo_qc_report.md` ← qc_report

## QC 判定

- ✅ Population denominator has 470 rows
- ✅ Population joins without missing prefecture-year pairs
- ✅ No ambiguous cell receives [1,9] count bounds
- ✅ No ambiguous cell receives a numeric rate bound
- ✅ Observed cells have equal lower and upper count/rate
- ✅ Primary low-count cells have count bounds [1,9]
- ✅ Naive ranking outputs are clearly labeled as comparison benchmarks
- ✅ Figure 4 data exist and are consistent with rate/ranking files

**最終判定: RATE_RANKING_DEMO_READY**

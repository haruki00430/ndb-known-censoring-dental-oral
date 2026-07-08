# Known Censoring「Dental/Oral」人口分母取得・Rate Bounds・Ranking Demo 詳細報告書

**作成日**: 2026年7月7日  
**プロジェクト**: Known Censoring, Not Missingness — NDB Open Data 既知検閲パイプライン検証研究  
**報告範囲**: `11Sonnet_Population_Rate_Bounds_Ranking_Demo_Prompt.md` に基づく人口分母取得（Step 1）・指標選択（Step 2）・Count Bounds（Step 3）・Rate Bounds（Step 4）・Ranking Stability（Step 5）・Naive Ranking Comparison（Step 6）・Figure 4 データ生成（Step 7）・QC レポート（Step 8）の全工程。**原稿 Results 本文の執筆は実施していない**  
**使用データ**: `results/full_extraction/` 内の CSV/JSON（Full Extraction 出力物）・e-Stat API・Statistics Bureau CSV。raw/ NDB ファイルへの再アクセスなし  
**実行エージェント**: claude-sonnet-4-6 (automated rate bounds + ranking demo)

---

## Executive Summary

| 項目 | 結果 |
|------|------|
| 人口分母行数 | **470**（10 年 × 47 都道府県）|
| 人口 join 欠損 | **0 件** |
| QC チェック数 | **8** |
| QC 通過数 | **8**（全 PASS）|
| ストップ条件トリガー | **0 件**（3 条件すべてクリア）|
| 選択指標数 | **3**（bounded_demo / stable_observed_demo / ambiguous_limit_demo）|
| Count Bounds 行数 | **1,410** |
| Rate Bounds 行数 | **1,410** |
| ambiguous セルへの数値境界付与 | **0 件**（ルール厳守）|
| Naive Ranking 行数 | **5,640**（4 戦略 × 1,410）|
| Figure 4 データ行数 | **2,068**（3 パネル）|
| **最終判定** | **RATE_RANKING_DEMO_READY** |

### **判定: 全 QC チェックが PASS。人口分母・レートバウンズ・ランキング安定性デモのデータが検証済み状態で論文 Figure 4 利用に供する**

> 歯科傷病 NDB Open Data（No.1–No.11、FY2021 除く 10 リリース）の既知検閲分析を、セル観測可能性・境界適格性から**レートバウンズ・ランキング安定性実証デモ**へ拡張した。人口分母は e-Stat および Statistics Bureau の一次ソースのみから取得（J-SSM パーケットは FY2019=FY2020 の同一値バグが判明したため不使用）。3 種の実証指標（血行性歯髄炎 / 根充済み / 限局型若年性歯周炎）に対し、observed セルは点識別レート、primary_low_count セルは区間 [1/pop×100k, 9/pop×100k] のレートバウンズ、ambiguous セルはレートバウンズなし（not_bounded_ambiguous）とした。全 8 QC チェックが PASS し、Figure 4 の 3 パネル（A: レートバウンズ、B: ランク区間、C: Naive 比較）のデータが生成された。Rate and ranking analyses are identification exercises. They show which regional comparisons are supported by the public release and disclosure rule, not recovered hidden counts.

---

## 1. 実行した作業の概要

### 1.1 データ非接触ルールの遵守確認

| ルール | 実施状況 |
|--------|---------|
| raw/ への書き込み禁止 | ✅ Full Extraction 出力 CSV/JSON のみを読み込み。raw/ への再アクセスなし |
| NDB 生データをAI に送信しない | ✅ 送信なし |
| 隠れた値の推定・補完禁止 | ✅ count/rate bounds は区間推定であり、隠れた値のモデルベース補完は行わない |
| ambiguous セルへの [1, 9] 付与禁止 | ✅ ambiguous/complementary 抑制セルへの数値境界割り当て: **0 件** |
| Full Extraction 出力ファイルの変更禁止 | ✅ Demo スクリプトは新規ファイルのみ生成。Full Extraction 出力は変更なし |

### 1.2 生成スクリプト・出力ファイル一覧

| スクリプト | 内容 |
|-----------|------|
| `scripts/step1_build_population_inventory.py` | 人口分母インベントリ構築（e-Stat 直接 DL + CSV）|
| `scripts/steps2_8_rate_bounds_demo.py` | Steps 2–8 一括（指標選択・Count/Rate Bounds・Ranking・Naive・Figure 4・QC）|

---

## 2. Step 1 — 人口分母インベントリ（470 行）

### 2.1 データソース選定の経緯

当初、J-SSM プロジェクトの `population_by_fy.parquet` を流用する案を検討したが、全都道府県で FY2019 値 = FY2020 値（例：鳥取県 FY2019=553,000 / FY2020=553,000 → 期待値 ~556,000 と ~553,000）という同一値バグが確認された。このため J-SSM パーケットは全面的に不使用とし、以下の一次ソースのみから人口分母を構築した。

### 2.2 使用ソース一覧

| FY | ソース | e-Stat テーブル / ファイル | 単位 | 変換 |
|---|---|---|---|---|
| FY2014 | e-Stat 人口推計 (H22/H26国勢調査基準) | `0003104195` (cdTime=2014001001) | **人** | 変換なし |
| FY2015 | e-Stat 人口推計 (H27国勢調査基準) | `0003459027` (cdTime=1501) | 千人 | ×1000 |
| FY2016 | 同上 | `0003459027` (cdTime=901) | 千人 | ×1000 |
| FY2017 | 同上 | `0003459027` (cdTime=1001) | 千人 | ×1000 |
| FY2018 | 同上 | `0003459027` (cdTime=1101) | 千人 | ×1000 |
| FY2019 | 同上 | `0003459027` (cdTime=1201) | 千人 | ×1000 |
| FY2020 | Statistics Bureau `pop_2023_est.csv` (R2基準) | time_code=1601 | 千人 | ×1000 |
| FY2021 | — | **除外**（No.8 指標変更）| — | — |
| FY2022 | Statistics Bureau `pop_2023_est.csv` (R2基準) | time_code=1701 | 千人 | ×1000 |
| FY2023 | 同上 | time_code=1801 | 千人 | ×1000 |
| FY2024 | 同上 | time_code=1901 | 千人 | ×1000 |

### 2.3 FY2014 の特記事項

e-Stat テーブル `0003104195` は 2013年10月1日と 2014年10月1日の推計値を格納しており、`@time=2014001001` かつ `@cat01=204, @cat02=000, @cat03=001`（総人口・男女計）でフィルタして 2014年10月1日の 47 都道府県値を取得した。単位は**人（×1000 変換不要）**。全国合計 = 127,082,819 人（統計局公表値と一致）。

### 2.4 人口推移サマリー

| FY | 都道府県数 | 最小（人）| 最大（人）| 備考 |
|---|---|---|---|---|
| 2014 | 47 | 573,940 | 13,389,725 | e-Stat 直接 DL（人）|
| 2015 | 47 | 573,000 | 13,515,000 | H27 基準（千人×1000）|
| 2016 | 47 | 570,000 | 13,624,000 | H27 基準 |
| 2017 | 47 | 565,000 | 13,724,000 | H27 基準 |
| 2018 | 47 | 560,000 | 13,822,000 | H27 基準 |
| 2019 | 47 | 556,000 | 13,921,000 | H27 基準（※J-SSM バグ値と異なる）|
| 2020 | 47 | 553,000 | 14,048,000 | R2 基準 |
| 2022 | 47 | 544,000 | 14,038,000 | R2 基準 |
| 2023 | 47 | 537,000 | 14,086,000 | R2 基準 |
| 2024 | 47 | 531,000 | 14,178,000 | R2 基準 |

> ※ J-SSM パーケットの FY2019 値は 556,000 ではなく 553,000（FY2020 値と同一）で誤りであった。

### 2.5 QC チェック結果（Step 1）

| チェック | 結果 |
|---------|------|
| 総行数 = 470（10 年 × 47 都道府県）| ✅ PASS |
| FY2021 が含まれていない | ✅ PASS |
| 全行で population > 0 かつ欠損なし | ✅ PASS |
| 各 FY 内で都道府県コードが 47 件・重複なし | ✅ PASS |
| FY2014 全国合計 = 127,082,819 人（公表値一致）| ✅ PASS |
| dental_cell_state_full.csv の都道府県コードと join 欠損なし | ✅ PASS（join 欠損 = 0）|

**出力**: `results/rate_bounds_demo/population_denominator_inventory.csv`（470 行 9 列）

---

## 3. Step 2 — 指標選択

### 3.1 選択基準

| 役割 | 選択条件 |
|------|---------|
| `bounded_demo` | primary_bounded_cells ≥ 3 かつ observed_cells ≥ 40 → primary_bounded_cells 降順で最上位 |
| `stable_observed_demo` | observed_cells / total_cells ≥ 95% かつ ambiguous_cells = 0 → observed_cells 降順で最上位（bounded_demo と重複不可）|
| `ambiguous_limit_demo` | ambiguous_suppression_cells ≥ 30 → ambiguous_cells 降順で最上位（上記 2 種と重複不可）|

### 3.2 候補数

| 役割 | 候補指標数 |
|------|---------|
| bounded_demo | 90 指標 |
| stable_observed_demo | 42 指標 |
| ambiguous_limit_demo | 106 指標 |

### 3.3 選択結果

| 役割 | indicator_id | 指標名 | observed | primary_bounded | ambiguous |
|------|---|---|---|---|---|
| bounded_demo | `IND_5220077` | **血行性歯髄炎** | 143 | **92** | 235 |
| stable_observed_demo | `IND_5210011` | **根充済み** | **470** | 0 | 0 |
| ambiguous_limit_demo | `IND_8843319` | **限局型若年性歯周炎** | 87 | 0 | **383** |

各指標は全 10 リリース（FY2014–2024 / No.8 除外）で利用可能（`retained_releases_available = 10`）。

**出力**: `results/rate_bounds_demo/demo_indicator_selection.csv`

---

## 4. Step 3 — Count Bounds

### 4.1 適用ルール

| cell_state | suppression_subtype | count_lower | count_upper | bounds_status | ambiguity_flag |
|---|---|---|---|---|---|
| observed | not_suppressed | 観測値 | 観測値 | point_identified | no |
| suppressed | primary_low_count | **1** | **9** | bounded_primary | no |
| suppressed | ambiguous_suppression | — (欠損) | — (欠損) | not_bounded_ambiguous | **yes** |

**原則**: ambiguous_suppression セルへの数値境界付与は一切行わない。

### 4.2 結果サマリー

| bounds_status | セル数 | 構成比（1,410 中）|
|---|---|---|
| point_identified（観測）| 700 | 49.6% |
| bounded_primary（[1,9]）| 92 | 6.5% |
| not_bounded_ambiguous | 618 | 43.8% |
| **合計** | **1,410** | 100% |

**QC 確認**: ambiguous セルに数値境界が付与されたケース = **0 件**

**出力**: `results/rate_bounds_demo/demo_count_bounds.csv`（1,410 行）

---

## 5. Step 4 — Rate Bounds

### 5.1 計算式

$$\text{rate per 100,000} = \frac{\text{count}}{{\text{population}}} \times 100{,}000$$

- observed: rate_lower = rate_upper = observed_count / population × 100,000（点識別）
- primary_low_count: rate_lower = 1 / population × 100,000、rate_upper = 9 / population × 100,000
- ambiguous_suppression: rate_lower = 欠損、rate_upper = 欠損、rate_status = `not_bounded_ambiguous`

### 5.2 結果サマリー

| rate_status | セル数 | 意味 |
|---|---|---|
| point_identified | 700 | 完全識別レート（observed セル）|
| bounded_primary | 92 | レート区間 [1/pop×100k, 9/pop×100k]（primary_low_count セル）|
| not_bounded_ambiguous | 618 | レートバウンズなし（ambiguous セル）|

### 5.3 指標別プロファイル

| 指標 | 役割 | point_identified | bounded_primary | not_bounded_ambiguous |
|---|---|---|---|---|
| 血行性歯髄炎 | bounded_demo | 143 | 92 | 235 |
| 根充済み | stable_observed_demo | 470 | 0 | 0 |
| 限局型若年性歯周炎 | ambiguous_limit_demo | 87 | 0 | 383 |

> 根充済み（`IND_5210011`）は 10 リリース × 47 都道府県 = 470 セルが全て observed → 全都道府県・全年度で点識別レートが得られる。血行性歯髄炎はレートバウンズ付き 92 件と not_bounded 235 件が混在する実証例。限局型若年性歯周炎は 383/470 = 81.5% が ambiguous でランキング不可の限界例示となる。

**QC 確認**:
- ambiguous セルに数値 rate 境界が付与されたケース = **0 件**
- observed セルで rate_lower ≠ rate_upper のケース = **0 件**

**出力**: `results/rate_bounds_demo/demo_rate_bounds.csv`（1,410 行）

---

## 6. Step 5 — Ranking Stability

### 6.1 ランキング方針

- point_identified セルおよび bounded_primary セルのみランク計算対象とする
- ambiguous セルはランク計算対象外（`ranking_not_supported_ambiguous`）
- ある指標-リリースペアに ambiguous セルが存在する場合、有効ランクは「全都道府県のうち rate 境界が得られた都道府県のみを対象とした部分ランキング」とし、全体ランキングは成立しないと表記する

### 6.2 ランキング計算ルール

| cell_state | ランク計算 |
|---|---|
| point_identified（ambiguous セルなし） | 全都道府県中の確定ランク → `stable_point_identified` |
| point_identified（同一 release 内に ambiguous あり）| 有効都道府県内での rank → `interval_ranked` |
| bounded_primary | rank_best = upper_rate より大きい都道府県数 + 1 / rank_worst = lower_rate 以上の都道府県数 → `interval_ranked` |
| ambiguous_suppression | ランク割り当て不可 → `ranking_not_supported_ambiguous` |

### 6.3 結果サマリー

| ranking_status | セル数 |
|---|---|
| stable_point_identified | 472 |
| interval_ranked | 320 |
| ranking_not_supported_ambiguous | 618 |
| **合計** | **1,410** |

> 根充済み（全セル observed）は全リリースで `stable_point_identified`（47 都道府県 × 10 リリース = 470 行 + α）。血行性歯髄炎の primary-bounded 92 行は `interval_ranked`（ランク区間幅 = rank_worst - rank_best）。限局型若年性歯周炎の 383 ambiguous 行は全て `ranking_not_supported_ambiguous`。

**出力**: `results/rate_bounds_demo/demo_ranking_stability.csv`（1,410 行）

---

## 7. Step 6 — Naive Ranking Comparison（比較ベンチマーク）

### 7.1 4 戦略の定義

| 戦略 | 抑制セルへの代入 | 根拠 | 警告 |
|---|---|---|---|
| complete_case | 除外（observed のみ使用）| — | 低カウント都道府県が除外され、選択バイアスが生じる可能性 |
| zero | 0 代入 | — | ゼロ代入は抑制規則と矛盾（count=0 は NDB 側で明示公開済み）。根拠なし |
| upper_bound_T_minus_1 | 9 代入（上限） | primary_low_count セルのみ理論的 | ambiguous セルへの T-1 適用は無効。点推定への変換は識別を過剰主張 |
| midpoint | 5 代入（中点）| primary_low_count セルのみ理論的 | ambiguous セルへの midpoint 適用は無効。点推定への変換は識別を過剰主張 |

**本分析における位置付け**: Naive 代入によるランキングは**比較ベンチマークのみ**であり、有効な統計的推論ではない。論文では Known Censoring アプローチとの対比のために提示する。

### 7.2 結果

- 総行数: **5,640**（1,410 セル × 4 戦略）
- strategy_warning 付与: 全行（100%）
- 戦略別に substituted_rank を算出（higher rate = lower rank number）

**出力**: `results/rate_bounds_demo/demo_naive_ranking_comparison.csv`（5,640 行）

---

## 8. Step 7 — Figure 4 データ生成

### 8.1 パネル構成

| パネル | 内容 | 使用指標 | 行数 |
|---|---|---|---|
| A_rate_bounds | 都道府県別レートバウンズの可視化 | 血行性歯髄炎 + 根充済み（各 10 リリース × 47 都道府県）| 940 |
| B_rank_intervals | ランク区間の可視化 | 血行性歯髄炎 + 根充済み | 940 |
| C_naive_comparison | Naive 代入ランキング比較 | 血行性歯髄炎（1 リリース × 47 都道府県 × 4 戦略）| 188 |
| **合計** | — | — | **2,068** |

### 8.2 パネル A：レートバウンズ

- `rate_status` によるセル分類（point_identified / bounded_primary / not_bounded_ambiguous）を都道府県軸で可視化するための source データ
- `rate_lower_per_100k` と `rate_upper_per_100k` の両列を含む（observed セルでは両者が等値）

### 8.3 パネル B：ランク区間

- `rank_best_possible` と `rank_worst_possible` からランク区間幅を可視化するための source データ
- `ranking_status` による色分け（stable_point_identified / interval_ranked / ranking_not_supported_ambiguous）

### 8.4 パネル C：Naive 比較

- 4 戦略のランク値を並べた比較用 source データ
- 各行に `strategy_warning` を付与（これが比較ベンチマークであることを明記）

**出力**: `figure_data/figure4_rate_bounds_ranking_demo.csv`（2,068 行）

---

## 9. Step 8 — QC レポート

### 9.1 8 チェック結果

| # | チェック | 判定 | 詳細 |
|---|---------|------|------|
| 1 | Population denominator has 470 rows | ✅ PASS | actual = 470 |
| 2 | Population joins without missing prefecture-year pairs | ✅ PASS | join 欠損 = 0 |
| 3 | No ambiguous cell receives [1,9] count bounds | ✅ PASS | 対象件数 = 0 |
| 4 | No ambiguous cell receives a numeric rate bound | ✅ PASS | 対象件数 = 0 |
| 5 | Observed cells have equal lower and upper count/rate | ✅ PASS | 不一致件数 = 0 |
| 6 | Primary low-count cells have count bounds [1,9] | ✅ PASS | 誤付与件数 = 0 / total = 92 |
| 7 | Naive ranking outputs are clearly labeled as comparison benchmarks | ✅ PASS | 全行に strategy_warning 付与 |
| 8 | Figure 4 data exist and are consistent with rate/ranking files | ✅ PASS | 2,068 行 / 3 パネル |

**ストップ条件トリガー: 0 件 → RATE_RANKING_DEMO_READY**

### 9.2 生成 QC ファイル

| ファイル | 内容 |
|---------|------|
| `results/rate_bounds_demo/rate_bounds_demo_qc_report.md` | 8 チェック詳細 QC レポート |
| `results/rate_bounds_demo/rate_bounds_demo_summary.json` | QC 結果の機械可読サマリー |
| `results/rate_bounds_demo/rate_bounds_demo_handoff_for_codex.md` | Codex 向けハンドオフノート |

---

## 10. ストップ条件の確認

| 条件 | トリガー |
|------|---------|
| `HOLD_POPULATION_SOURCE_NEEDED`：公式人口分母が取得できない / 470 行未満 | ✅ なし（470 行・全て公式ソース）|
| `HOLD_RATE_BOUNDS_QC_FAILED`：ambiguous セルに数値境界 / population join 欠損 / 不適切なランキング | ✅ なし（全 QC チェック PASS）|
| `RATE_RANKING_DEMO_READY`：全条件クリア | **該当（最終判定）**|

---

## 11. J-SSM パーケット FY2019 バグについて

J-SSM プロジェクトの `population_by_fy.parquet` において、FY2019 と FY2020 の値が全 47 都道府県で一致することを発見した。具体例：

| 都道府県 | J-SSM FY2019 | J-SSM FY2020 | e-Stat FY2019（正規値） |
|---------|---|---|---|
| 鳥取県 | 553,000 人 | 553,000 人 | 556,000 人（H27基準）|
| 東京都 | 14,048,000 人 | 14,048,000 人 | 13,921,000 人（H27基準）|

原因: J-SSM スクリプト (`03b_extend_population_panel.py`) が FY2019 の H27 基準推計値の取得に失敗し、FY2020 の R2 基準値で代替したと推定される。本プロジェクトでは一次ソース（e-Stat 0003459027）から FY2019 を直接取得することで回避した。NDB 研究全般において J-SSM パーケットの FY2019 人口を使用する場合は要注意。

---

## 12. 論文 Results・Methods に使える発見

| 発見 | 論文利用先 |
|------|-----------|
| 人口分母: 470 行・全年度 join 欠損ゼロ・公式一次ソースのみ | Methods（人口分母の記述）|
| 根充済みは全 470 セルが observed → 完全識別レート（全都道府県・全年度）| Results Figure 4A/4B（stable_observed_demo）|
| 血行性歯髄炎は primary_bounded 92 件のレート区間 [1/pop×100k, 9/pop×100k] が計算可能 | Results Figure 4A/4B（bounded_demo）|
| 限局型若年性歯周炎は ambiguous 383/470（81.5%）でレートバウンズ・ランキング不可 | Results Figure 4A/4B（ambiguous_limit_demo）|
| ambiguous セルへの数値境界付与 = 0 件（ルール厳守）| Methods（既知検閲 vs 曖昧抑制の区別）|
| Naive 代入（zero/upper_bound_T-1/midpoint）は全ての ambiguous セルに適用不能 | Discussion（naive handling の限界）|
| primary_bounded ランク区間の幅はレートバウンズの幅に比例（人口の逆数で変動）| Results（ランキング安定性の記述）|

---

## 13. 生成ファイル一覧（完全）

| 場所 | ファイル名 | サイズ | 内容 |
|------|-----------|--------|------|
| `scripts/` | `step1_build_population_inventory.py` | — | 人口分母構築スクリプト |
| `scripts/` | `steps2_8_rate_bounds_demo.py` | — | Steps 2–8 一括スクリプト |
| `results/rate_bounds_demo/` | `population_denominator_inventory.csv` | 160 KB | 470 行（10 年 × 47 都道府県）|
| `results/rate_bounds_demo/` | `demo_indicator_selection.csv` | 0.5 KB | 3 指標の選択根拠 |
| `results/rate_bounds_demo/` | `demo_count_bounds.csv` | 167 KB | Count Bounds（1,410 行）|
| `results/rate_bounds_demo/` | `demo_rate_bounds.csv` | 181 KB | Rate Bounds（1,410 行）|
| `results/rate_bounds_demo/` | `demo_ranking_stability.csv` | 195 KB | Ranking Stability（1,410 行）|
| `results/rate_bounds_demo/` | `demo_naive_ranking_comparison.csv` | 1.37 MB | Naive Ranking（5,640 行）|
| `results/rate_bounds_demo/` | `rate_bounds_demo_qc_report.md` | 3 KB | 8 チェック QC レポート |
| `results/rate_bounds_demo/` | `rate_bounds_demo_summary.json` | 4.2 KB | 機械可読 QC サマリー |
| `results/rate_bounds_demo/` | `rate_bounds_demo_handoff_for_codex.md` | 2.9 KB | Codex ハンドオフノート |
| `figure_data/` | `figure4_rate_bounds_ranking_demo.csv` | 260 KB | Figure 4 source（2,068 行・3 パネル）|
| `docs/` | `Dental_Oral_Rate_Bounds_Ranking_Demo_Report_20260707.md` | — | 本報告書 |
| `docs/` | `Dental_Oral_Rate_Bounds_Ranking_Demo_Summary_20260707.md` | — | 本報告書に対応するサマリー |

---

## 14. 次ステップ

| ステップ | 内容 | 状態 |
|---------|------|------|
| ✅ パイロット実行 | 2 指標 × 3 リリース × 39 セル | **完了** |
| ✅ Full Extraction 実行 | 311 指標 × 10 リリース × 71,017 セル | **完了** |
| ✅ QC 監査 + 論文用テーブル生成 | 8 チェック PASS・Table 1–4・Figure 1–3 | **完了** |
| ✅ **人口分母 + Rate Bounds + Ranking Demo** | **8 チェック PASS・Figure 4 データ生成 → RATE_RANKING_DEMO_READY** | **完了（本文書）**|
| ⏳ 論文 Methods・Results 本文執筆 | Table 1–4・Figure 1–4 を用いた原稿作成 | **次フェーズ** |
| ⏳ 他ドメイン（医科・処方薬）への拡張 | 同パイプラインを医科傷病・処方薬ファイルに適用 | **将来フェーズ** |

---

*本報告書は `11Sonnet_Population_Rate_Bounds_Ranking_Demo_Prompt.md` に基づく人口分母取得・Rate Bounds・Ranking Demo（2026-07-07）の記録である。*  
*raw/ の NDB データへの再アクセスなし。Full Extraction 出力 CSV/JSON のみを source of truth として使用。ambiguous suppressionセルへの数値境界付与なし。隠れた値の推測・補完は実施していない。*

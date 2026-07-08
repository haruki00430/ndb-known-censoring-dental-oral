# Known Censoring「Dental/Oral」人口分母取得・Rate Bounds・Ranking Demo サマリー

**作成日**: 2026年7月7日  
**対象読者**: プロジェクト管理者・共著者  
**対応する詳細報告書**: `docs/Dental_Oral_Rate_Bounds_Ranking_Demo_Report_20260707.md`

---

## この作業は何のためにやったのか

QC 監査 + 論文用テーブル生成（Step 3）で確認した 71,017 セルのデータから、論文の実証デモとして「**公開リリースと開示規則によって支持される地域比較の範囲（partial identification）**」を示すため、都道府県別レートバウンズとランキング安定性デモを実施した。具体的には、都道府県別人口分母（470 行）を公式一次ソースから取得し、3 種の代表指標に対して (1) observed セルの点識別レート・(2) primary_low_count セルのレート区間・(3) ambiguous セルでのランキング不可事例を生成して Figure 4 の source データとした。

---

## 今回やったこと

1. **人口分母インベントリ構築**（e-Stat 0003104195 / 0003459027・Statistics Bureau pop_2023_est.csv から 10 年 × 47 都道府県 = 470 行を取得）
2. **J-SSM パーケットのバグ発見と一次ソース直接取得への切り替え**（FY2019=FY2020 の同一値バグを確認、全面的に e-Stat 直接 DL で回避）
3. **実証指標の選択**（90 候補から bounded_demo・42 候補から stable_observed_demo・106 候補から ambiguous_limit_demo を各 1 指標選択）
4. **Count Bounds 計算**（1,410 セル：point_identified=700 / bounded_primary=92 / not_bounded_ambiguous=618）
5. **Rate Bounds 計算**（count / population × 100,000。ambiguous セルへの数値境界付与: 0 件）
6. **Ranking Stability デモ**（stable_point_identified=472 / interval_ranked=320 / ranking_not_supported=618）
7. **Naive Ranking 比較**（complete_case / zero / upper_bound_T-1 / midpoint の 4 戦略・5,640 行、全行に比較ベンチマーク警告付与）
8. **Figure 4 データ生成**（3 パネル 2,068 行：A=レートバウンズ・B=ランク区間・C=Naive 比較）
9. **QC レポート**（8 チェック全 PASS、RATE_RANKING_DEMO_READY）

---

## 結果サマリー

### QC 8 チェックの結果

| チェック | 内容 | 判定 |
|---------|------|------|
| 1. 人口分母行数 | 470 行（10 年 × 47 都道府県）| ✅ PASS |
| 2. Population join | 欠損 = 0 件 | ✅ PASS |
| 3. ambiguous に count bounds なし | 対象件数 = 0 | ✅ PASS |
| 4. ambiguous に rate bounds なし | 対象件数 = 0 | ✅ PASS |
| 5. observed セルの lower = upper | 不一致 = 0 件 | ✅ PASS |
| 6. primary_low_count に [1, 9] | 誤付与 = 0 件 / 合計 92 件 | ✅ PASS |
| 7. Naive ランキングの警告付与 | 全行に strategy_warning | ✅ PASS |
| 8. Figure 4 データの存在確認 | 2,068 行・3 パネル | ✅ PASS |

### 人口分母のソース一覧

| FY | ソース | 単位変換 |
|---|---|---|
| FY2014 | e-Stat table 0003104195（H22/H26基準、直接 DL） | なし（単位=人）|
| FY2015–2019 | e-Stat table 0003459027（H27基準、直接 DL） | 千人 × 1000 |
| FY2020,2022–2024 | `pop_2023_est.csv`（R2基準）| 千人 × 1000 |
| FY2021 | 除外（No.8 指標変更）| — |

### 選択指標（3 種）

| 役割 | indicator_id | 指標名 | observed | primary_bounded | ambiguous |
|------|---|---|---|---|---|
| bounded_demo | IND_5220077 | 血行性歯髄炎 | 143 | 92 | 235 |
| stable_observed_demo | IND_5210011 | 根充済み | 470 | 0 | 0 |
| ambiguous_limit_demo | IND_8843319 | 限局型若年性歯周炎 | 87 | 0 | 383 |

### Rate Bounds・Ranking 結果

| 区分 | Rate Status | セル数 | Ranking Status | セル数 |
|------|---|---|---|---|
| observed セル | point_identified | 700 | stable_point_identified | 472 |
| primary_low_count セル | bounded_primary | 92 | interval_ranked | 320 |
| ambiguous セル | not_bounded_ambiguous | 618 | ranking_not_supported_ambiguous | 618 |

### 生成したファイル（12 ファイル）

| カテゴリ | ファイル | 内容 |
|---------|---------|------|
| スクリプト | `scripts/step1_build_population_inventory.py` | 人口分母構築 |
| スクリプト | `scripts/steps2_8_rate_bounds_demo.py` | Steps 2–8 一括 |
| Demo | `results/rate_bounds_demo/population_denominator_inventory.csv` | 470 行 |
| Demo | `results/rate_bounds_demo/demo_indicator_selection.csv` | 3 指標 |
| Demo | `results/rate_bounds_demo/demo_count_bounds.csv` | 1,410 行 |
| Demo | `results/rate_bounds_demo/demo_rate_bounds.csv` | 1,410 行 |
| Demo | `results/rate_bounds_demo/demo_ranking_stability.csv` | 1,410 行 |
| Demo | `results/rate_bounds_demo/demo_naive_ranking_comparison.csv` | 5,640 行 |
| QC | `results/rate_bounds_demo/rate_bounds_demo_qc_report.md` | 8 チェック詳細 |
| QC | `results/rate_bounds_demo/rate_bounds_demo_summary.json` | 機械可読サマリー |
| QC | `results/rate_bounds_demo/rate_bounds_demo_handoff_for_codex.md` | Codex ハンドオフ |
| Figure データ | `figure_data/figure4_rate_bounds_ranking_demo.csv` | 2,068 行・3 パネル |

---

## 注記事項

| 項目 | 内容 |
|------|------|
| **最終判定** | **RATE_RANKING_DEMO_READY**（ストップ条件 0 件トリガー）|
| **J-SSM パーケット不使用** | FY2019 と FY2020 が全都道府県で同一値（バグ）。e-Stat 直接 DL で回避 |
| **FY2014 注記** | e-Stat 0003104195 は cat03=001（総人口）/ cat03=002（日本人人口）の 2 値あり。cat03=001 を選択（国内合計 127,082,819 人で公表値と一致確認）|
| **FY2019 正規値** | H27基準 e-Stat 取得値：鳥取県 556,000 人、東京都 13,921,000 人（J-SSM バグ値 553,000 / 14,048,000 とは異なる）|
| **ambiguous セル** | いかなる数値境界も受け取っていない（Count / Rate / Ranking すべてで 0 件確認）|
| **Naive 代入の位置付け** | 比較ベンチマークのみ。有効な統計的推論ではない。全行に `strategy_warning` 付与 |
| **raw/ アクセス** | なし（Full Extraction 出力 CSV/JSON + e-Stat API + Statistics Bureau CSV のみ使用）|

---

## 現在のステップ管理

| ステップ | 内容 | 状態 |
|---------|------|------|
| 1. パイロット実行 | 2 指標 × 3 リリース × 39 セル | ✅ 完了 |
| 2. Full Extraction 実行 | 311 指標 × 10 リリース × 71,017 セル | ✅ 完了 |
| 3. QC 監査 + テーブル生成 | 8 チェック PASS・Table 1–4・Figure 1–3 | ✅ 完了 |
| **4. 人口分母 + Rate Bounds + Ranking Demo** | **8 チェック PASS・Figure 4 → RATE_RANKING_DEMO_READY** | ✅ **完了（本文書）** |
| 5. 論文 Methods / Results 本文執筆 | Table 1–4・Figure 1–4 を用いた原稿作成 | ⏳ 次フェーズ |
| 6. 他ドメイン拡張 | 医科傷病・処方薬への同パイプライン適用 | ⏳ 将来 |

---

*本サマリーは `11Sonnet_Population_Rate_Bounds_Ranking_Demo_Prompt.md` に基づく人口分母取得・Rate Bounds・Ranking Demo（2026-07-07）の非技術サマリーである。*  
*raw/ の NDB データへの再アクセスなし。ambiguous suppression セルへの数値境界付与なし。隠れた値の推測・補完は実施していない。*

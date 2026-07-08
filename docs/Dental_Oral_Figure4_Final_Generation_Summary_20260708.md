# Known Censoring「Dental/Oral」Figure 4 最終生成 サマリー

**作成日**: 2026年7月8日  
**対象読者**: プロジェクト管理者・共著者  
**対応する詳細報告書**: `docs/Dental_Oral_Figure4_Final_Generation_Report_20260708.md`

---

## この作業は何のためにやったのか

2026-07-07 の Rate Bounds・Ranking Demo（Step 4）で生成した Figure 4 source CSV（`figure_data/figure4_rate_bounds_ranking_demo.csv`）を使い、論文に直接投稿できる水準の **Figure 4 最終 PNG/SVG** を生成するため。ワークオーダー `15_12Sonnet_Figure4_CSV_Retrieval_and_Final_Figure_Work_Order.md` に従い、QC 10 チェックを通過させてから図を出力した。

---

## 今回やったこと

1. **Figure 4 source CSV の所在確認**（`figure_data/figure4_rate_bounds_ranking_demo.csv` — 259,648 バイト・既存ファイル）
2. **支援ファイル 9 件の存在確認**（`results/rate_bounds_demo/` 内の全ファイル — 全件存在）
3. **QC 10 チェック実施**（全 PASS → `HOLD_FIGURE4_QC_FAILED` 条件に非該当）
4. **最終図ファイルの生成**（PNG 867 KB / SVG 591 KB — 300 dpi、20×32 インチ、3パネル）
5. **キャプション・Results 参照文の整備**（`outputs/figure4_rate_bounds_ranking_demo_final_caption.md`）
6. **QC レポートの出力**（`outputs/figure4_rate_bounds_ranking_demo_final_qc.md`）

---

## 結果サマリー

### QC 10 チェックの結果

| チェック | 内容 | 判定 |
|---------|------|------|
| 1. CSVファイル存在 | `figure_data/figure4_rate_bounds_ranking_demo.csv` | ✅ PASS |
| 2. 総行数 | 2,068 行 | ✅ PASS |
| 3. パネル行数 | A=940 / B=940 / C=188 | ✅ PASS |
| 4. Panel A ambiguous 数値境界なし | 対象: **0 件** | ✅ PASS |
| 5. Panel B ranking\_not\_supported 数値ランクなし | 対象: **0 件** | ✅ PASS |
| 6. Panel C 全行にベンチマーク警告ラベル | naive\_ プレフィックス: 188/188 行 | ✅ PASS |
| 7. Observed セル lower = upper | 不一致: **0 件** | ✅ PASS |
| 8. bounded\_primary 全件で lower < upper の区間 | 92/92 件 | ✅ PASS |
| 9. ambiguous セルへの推論なし（check 4+5 再確認）| 数値付与: **0 件** | ✅ PASS |
| 10. 選択指標が 7/7 報告書と一致 | IND\_5210011 + IND\_5220077 | ✅ PASS |

### 図のデザイン（3パネル構成）

| パネル | 内容 | 列・行構成 |
|--------|------|----------|
| **Panel A** | 都道府県別レートバウンズ（per 100,000 人）| 3 列 × 47 都道府県 |
| **Panel B** | 都道府県別ランク区間 | 3 列 × 47 都道府県 |
| **Panel C** | Naive ランキング戦略比較 [BENCHMARK ONLY] | 全幅 × 47 都道府県 × 4 戦略 |

#### Panel A / B の3列構成

| 列 | 指標 | FY / リリース | 主なセル状態 | 示す内容 |
|----|------|---|---|---|
| **A1 / B1** | 血行性歯髄炎 | FY2016 / No.3（積極的ルール）| bounded\_primary 46件 + 観測 1件 | レート区間がある場合 |
| **A2 / B2** | 血行性歯髄炎 | FY2023 / No.10（標準ルール）| 観測 45件 + ambiguous 2件 | 観測主体＋境界付与不可 |
| **A3 / B3** | 根充済み | FY2023（参照指標）| 観測 47件（全件）| 完全識別可能な参照 |

この3列構成により、単一の FY では表現できない「3種全てのセル状態（点識別・区間識別・境界付与不可）」を1図で示した。

#### Panel C の意義

No.1 / FY2014 は missing suppression ルールを採用しており、46/47 都道府県が `not_bounded_ambiguous`（primary か complementary か不明）。4 つの naive 戦略（complete\_case / zero / upper\_bound\_T-1 / midpoint）はいずれも縮退した分布（多くの都道府県が rank=1 に集中 or NaN）を生み出し、ランキング情報を提供しない。これが「missing ルール年度での naive 代入が無効である」ことの直接的な視覚的証拠。

### 生成ファイル（`outputs/`）

| ファイル | サイズ | 内容 |
|---------|--------|------|
| `figure4_rate_bounds_ranking_demo_final.png` | **867 KB** | 論文用最終図（300 dpi）|
| `figure4_rate_bounds_ranking_demo_final.svg` | **591 KB** | 論文用最終図（SVG）|
| `figure4_rate_bounds_ranking_demo_final_caption.md` | **2.9 KB** | 公式キャプション・Results 参照文・Limitation 補足 |
| `figure4_rate_bounds_ranking_demo_final_qc.md` | **3.5 KB** | QC 10 チェック詳細レポート |

---

## 注記事項

| 項目 | 内容 |
|------|------|
| **最終判定** | **FIGURE4\_FINAL\_READY**（ストップ条件 0 件トリガー）|
| **`strategy_warning` カラム不在** | Panel C の CSV に `strategy_warning` カラムは存在しないが、全 188 行の `ranking_status` が `naive_*` プレフィックスを保持しており、QC Check 6 を機能的に満たす |
| **アグリゲート Draft の廃止推奨** | `outputs/figure4_known_censoring_aggregate_draft.png` は本 PNG で置き換え。manuscript module の Figure 4 参照先を更新する必要あり |
| **ambiguous セルへの数値境界付与** | いかなる数値境界も受け取っていない（Count / Rate / Ranking すべてで 0 件確認）|
| **Naive 代入の位置付け** | 比較ベンチマークのみ。有効な統計的推論ではない。Panel C に「BENCHMARK ONLY — NOT VALID INFERENCE」警告バナー付与済み |
| **raw/ アクセス** | なし（Figure 4 source CSV + 支援 CSV/JSON のみ使用）|
| **スクリプトの永続化** | 生成スクリプト（`generate_figure4_final.py`）はセッション一時領域に保存。必要に応じて `scripts/` へ移動を推奨 |

---

## 現在のステップ管理

| ステップ | 内容 | 状態 |
|---------|------|------|
| 1. パイロット実行 | 2 指標 × 3 リリース × 39 セル | ✅ 完了 |
| 2. Full Extraction 実行 | 311 指標 × 10 リリース × 71,017 セル | ✅ 完了 |
| 3. QC 監査 + テーブル生成 | 8 チェック PASS・Table 1–4・Figure 1–3 | ✅ 完了 |
| 4. 人口分母 + Rate Bounds + Ranking Demo | 8 チェック PASS・Figure 4 データ生成 | ✅ 完了 |
| **5. Figure 4 最終生成** | **10 チェック PASS・PNG/SVG/caption/QC 生成** | ✅ **完了（本文書）** |
| 6. 論文 Methods / Results 本文執筆 | Table/Figure を使った原稿作成 | ⏳ 次フェーズ |
| 7. 他ドメイン拡張 | 医科傷病・処方薬への同パイプライン適用 | ⏳ 将来 |

---

*本サマリーは `15_12Sonnet_Figure4_CSV_Retrieval_and_Final_Figure_Work_Order.md` に基づく Figure 4 最終生成（2026-07-08）の非技術サマリーである。*  
*raw/ の NDB データへの再アクセスなし。ambiguous suppression セルへの数値境界付与なし。隠れた値の推測・補完は実施していない。*

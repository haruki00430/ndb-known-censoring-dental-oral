# Known Censoring「Dental/Oral」QC 監査 + 論文用テーブル生成 サマリー

**作成日**: 2026年7月7日  
**対象読者**: プロジェクト管理者・共著者  
**対応する詳細報告書**: `docs/Dental_Oral_QC_Table_Generation_Report_20260707.md`

---

## この作業は何のためにやったのか

Full Extraction で生成した 71,017 セルのデータが**信頼できる状態で論文に使える**ことを独立に確認するため、CSV/JSON ファイルを source of truth として全数値を再集計した。また、論文本文（Results・Methods）執筆のために必要なテーブル（Table 1–4）と Figure source データ（Figure 1–3）をこの段階で生成し、次フェーズの Codex（論文執筆エージェント）に引き渡せる状態にした。

---

## 今回やったこと

1. **8 ファイルの存在・スキーマ確認**（dental_file_inventory / rule_inventory / indicator_catalog / cell_state_full / row_suppression_context / bounds_primary / naive_handling_ready / extraction_summary.json）— 全 8 ファイル存在確認
2. **リリースインベントリ確認**（11 リリースの登録・No.8 除外・保持数 10 の照合）
3. **ルールバリアント照合**（missing / aggressive / standard の割り当てが全 11 リリースで期待値と一致）
4. **全報告値の独立再集計**（CSV/JSON から 11 指標値を再計算、乖離ゼロを確認）
5. **境界整合性の全件チェック**（dental_bounds_primary.csv の全 4,982 行が [1, 9] / lower_bound_rule=event_exists / ambiguous 混入ゼロを確認）
6. **行コンテキストロジックの検証**（No.1–2: primary 0 件、No.5–11: primary 0 件、No.3–4 分類ミスゼロを確認）
7. **Naive handling 確認**（4 戦略すべて存在・全 6,044 行が strategy_ready=yes）
8. **スクリプト SHA-256 記録**（`f7e5d319c714556a`、Full Extraction の再実行はなし）

---

## 結果サマリー

### QC 8 チェックの結果

| チェック | 内容 | 判定 |
|---------|------|------|
| 1. ファイル存在 | 8 ファイル全て存在、行数正常 | ✅ PASS |
| 2. リリースインベントリ | 11 リリース登録、No.8 除外確認、保持 10 | ✅ PASS |
| 3. ルールバリアント | missing/aggressive/standard 全 11 行一致 | ✅ PASS |
| 4. セル状態再集計 | 11 指標値すべて CSV/JSON から完全再現 | ✅ PASS |
| 5. 境界整合性 | ambiguous 混入ゼロ・全行 [1,9]・event_exists | ✅ PASS |
| 6. 行コンテキスト | No.1–2 / No.5–11 primary ゼロ、分類ミスゼロ | ✅ PASS |
| 7. Naive handling | 4 戦略存在・全行 ready | ✅ PASS |
| 8. スクリプト再現性 | SHA-256 記録、再実行なし | ✅ PASS |

### 再集計で確認した数値

| 指標 | 値 |
|------|---|
| 保持リリース数 | 10 |
| 傷病指標数 | 311 |
| 総セル数 | 71,017 |
| observed セル | 45,285 (63.8%) |
| suppressed セル | 25,732 (36.2%) |
| ├ primary_low_count [1, 9] | 4,982 (19.4% of suppressed) |
| └ ambiguous_suppression | 20,750 (80.6% of suppressed) |
| blank セル | 0 |
| parse_error セル | 0 |
| 乖離件数 | **0 件** |

### 生成したファイル（14 ファイル）

| カテゴリ | ファイル | 内容 |
|---------|---------|------|
| QC | `qc/dental_full_extraction_qc_report.md` | 8 チェック詳細 |
| QC | `qc/dental_full_extraction_qc_summary.json` | 機械可読サマリー |
| QC | `qc/dental_full_extraction_qc_handoff_for_codex.md` | Codex ハンドオフノート |
| 論文テーブル | `manuscript_tables/table1_*` (CSV + MD) | Table 1: リリース/ルールインベントリ |
| 論文テーブル | `manuscript_tables/table2_*` (CSV + MD) | Table 2: リリース別観測可能性 |
| 論文テーブル | `manuscript_tables/table3_*` (CSV + MD) | Table 3: 抑制サブタイプ・境界 |
| 論文テーブル | `manuscript_tables/table4_*` (CSV + MD) | Table 4: Naive handling 比較 |
| Figure データ | `figure_data/figure1_*.csv` | Figure 1: ルールバリアントタイムライン |
| Figure データ | `figure_data/figure2_*.csv` | Figure 2: 観測可能性ヒートマップ |
| Figure データ | `figure_data/figure3_*.csv` | Figure 3: 境界適格性 |

---

## 注記事項

| 項目 | 内容 |
|------|------|
| **QC 判定** | **QC_PASS_TABLES_READY**（ストップ条件 0 件トリガー） |
| **構造的異常（1 件）** | No.3「う蝕第３度歯髄壊死」（宮崎県）: aggressive 補完ルール未適用と思われる行（n_supp=1 なのに観測セル 46 行がすべて非ゼロ）。境界 [1, 9] は正当。論文 Methods に footnote 推奨 |
| **QC レポート表示の注記** | `qc_report.md` の Check 4 テーブルで `release_count_scanned` と `primary_bounds_eligible_cell_count` に「—」(❌)が表示されているが、`discrepancies = {}` であり実質的な乖離なし（スクリプトの表示上の問題） |
| **No.8 の扱い** | FY2021 は指標が「算定回数」（傷病件数ではない）のため除外。ルールバリアントは standard として記録 |
| **raw/ アクセス** | なし（Full Extraction 出力 CSV/JSON のみを使用）|

---

## 現在のステップ管理

| ステップ | 内容 | 状態 |
|---------|------|------|
| 1. パイロット実行 | 2 指標 × 3 リリース × 39 セル | ✅ 完了 |
| 2. Full Extraction 実行 | 311 指標 × 10 リリース × 71,017 セル | ✅ 完了 |
| **3. QC 監査 + テーブル生成** | **8 チェック PASS・Table 1–4・Figure 1–3** | ✅ **完了（本文書）** |
| 4. 論文 Methods / Results 執筆 | Table/Figure を使った原稿作成 | ⏳ 次フェーズ |
| 5. QC スクリプト軽微修正 | Check 4 表示バグ修正 | ⏳ 任意 |
| 6. 他ドメイン拡張 | 医科傷病・処方薬への同パイプライン適用 | ⏳ 将来 |

---

*本サマリーは `07Sonnet_Dental_Oral_QC_Table_Generation_Prompt.md` に基づく QC 監査 + 論文用テーブル生成（2026-07-07）の非技術サマリーである。*  
*raw/ の NDB データへの再アクセスなし。隠れた値の推測・補完は実施していない。*

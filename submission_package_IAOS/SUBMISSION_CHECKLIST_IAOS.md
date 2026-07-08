# 投稿最終チェックリスト — Statistical Journal of the IAOS (Sage)

**論文タイトル**: Known Censoring, Not Missingness: Cell Suppression and Partial Identification in Open Administrative Healthcare Data  
**投稿先**: Statistical Journal of the IAOS (Sage)  
**作成日**: 2026-07-08  
**ステータス**: ⏳ 投稿準備中

---

## A. 原稿完成チェック（v0.8ベース）

### 文字数・構成（QA確認済み）
- [x] Abstract: **250語** ✅
- [x] 本文（Introduction〜Conclusions）: **2,798語** ✅
- [x] Tables: **4点** (Table 1–4) ✅
- [x] Main Figure: **1点** (Figure 1) ✅
- [x] Supplementary: Tables S1–S2 + Figure S1 ✅
- [x] References: **18件**（Vancouver番号形式）✅

### 原稿内容（構造QA確認済み）
- [x] "This draft" / "Draft status" / "Date:" 等の残留なし ✅
- [x] Figure 3 / Figure 4 の残留参照なし ✅
- [x] 旧画像パスの残留なし ✅
- [x] Word コメント / 変更追跡マークアップなし ✅
- [x] キーワード記載あり ✅

### 残り作業（投稿前に必須）
- [ ] **著者貢献（CRediT）記入** → `author_contributions_CRediT.md` 参照
- [ ] **著者名・所属・ORCID 記入**（カバーレター・CITATION.cff・README の全プレースホルダー）
- [ ] **データ公開文 更新** → GitHub URL + Zenodo DOI を記入（`data_availability_update_note.md` 参照）
- [ ] **GitHub リポジトリ作成・公開** → `haruki00430/ndb-known-censoring-dental-oral`
- [ ] **Zenodo リリース作成・DOI 取得**
- [ ] DOCX 原稿の著者貢献・データ公開文を最終版に更新

---

## B. 投稿ファイル一覧（Sage 投稿システム向け）

| ファイル | 種別ラベル（想定） | 状態 |
|---------|-----------------|------|
| `Known_Censoring_Not_Missingness_integrated_draft_v0_8.docx` | Main manuscript | ✅ 存在 |
| `Known_Censoring_Not_Missingness_supplement_v0_8.docx` | Supplementary material | ✅ 存在 |
| `cover_letter_IAOS.md` → DOCX変換 | Cover letter | ✅ ドラフト完成（著者情報要記入）|
| `v0_8_submission_final/figure1_rate_bounds_ranking_support_main.png` | Figure 1 (main) | ✅ 存在 |
| `v0_8_submission_final/supplementary_figure_s1_naive_ranking.png` | Supplementary Figure S1 | ✅ 存在 |

### ポリシーPDF（署名済み前提）
- [ ] `Declaration of conflicting interests-1.pdf` 〜 `-4.pdf`（全著者分）
- [ ] `Ethics approval and informed consent statements-1.pdf` 〜 `-4.pdf`（全著者分）
- [ ] `Funding statements.pdf`
- [ ] `Research data sharing policies.pdf`
- [ ] `Artificial intelligence policy.pdf`
- [ ] `Authorship guidelines.pdf`（確認のみ）
- [ ] `Simultaneous submissions policy.pdf`（確認のみ）

---

## C. 宣言文チェック（IAOS/Sage 標準）

| 項目 | 内容 | 状態 |
|-----|------|------|
| Ethics | 公開集計データのみ・倫理審査不要 | ✅ 記載済み |
| COI | "The authors declare no conflicts of interest." | ✅ 記載済み |
| Funding | "No specific funding was received for this work." | ✅ 記載済み |
| Data availability | GitHub + Zenodo URL（要記入） | ⏳ URL 未記入 |
| Author contributions | CRediT（要記入） | ⏳ 未記入 |
| AI利用開示 | Sage の AI policy PDF に従い記入 | ⏳ PDF 署名要確認 |
| Acknowledgments | "None." | ✅ 記載済み |

---

## D. Figure チェック

| Figure | ファイル | 解像度 | 言語 | 状態 |
|--------|--------|-------|------|------|
| Figure 1 | `figure1_rate_bounds_ranking_support_main.png` | 要確認 | 要確認 | ⚠️ 要目視確認 |
| Figure S1 | `supplementary_figure_s1_naive_ranking.png` | 要確認 | 要確認 | ⚠️ 要目視確認 |
| Figure 4 v2（代替案）| `outputs/figure4_rate_bounds_ranking_demo_final_v2.png` | 300 dpi | 英語 | ✅ 確認済み |

> **注意**: Figure 1 / S1 は別エージェントが生成。英語表記・解像度（300 dpi 以上）を目視確認のうえ、必要に応じて Figure 4 v2 で置き換えを検討してください。

---

## E. GitHub リポジトリ整備チェック

| ファイル | パス | 状態 |
|---------|------|------|
| README（日英） | `README_github.md` → リポジトリ root に `README.md` | ✅ ドラフト完成 |
| CITATION.cff | `CITATION.cff` | ✅ ドラフト完成（著者情報要記入）|
| LICENSE | `LICENSE` (CC BY 4.0) | ✅ 完成 |
| REPRODUCE.md | `REPRODUCE.md` | ✅ 完成 |
| .gitignore | `.gitignore` | ⏳ 未確認（既存 Hub の .gitignore 適用？）|
| スクリプト | `scripts/` | ✅ 既存 |
| 解析結果 CSV | `results/rate_bounds_demo/` | ✅ 既存 |
| Figure source CSV | `figure_data/figure4_rate_bounds_ranking_demo.csv` | ✅ 既存 |

### Git 操作手順
```bash
# プロジェクトフォルダで git init
cd projects/NDB-dental-oral-20260707
git init
git add README.md CITATION.cff LICENSE REPRODUCE.md scripts/ figure_data/ results/rate_bounds_demo/ manuscript_tables/ outputs/figure4_rate_bounds_ranking_demo_final_v2.png
git commit -m "feat: initial public release — known censoring dental/oral analysis"

# GitHub remote を追加してプッシュ
git remote add origin https://github.com/haruki00430/ndb-known-censoring-dental-oral.git
git push -u origin main
```

---

## F. Zenodo 登録手順

1. Zenodo (https://zenodo.org/) にログイン
2. "New upload" → GitHub リポジトリを連携
3. バージョン v1.0.0 でリリース作成
4. DOI を取得 → `CITATION.cff` と原稿 Data availability 文に記入

---

## G. 共著者通知メール（投稿後）

投稿完了後、以下を大平先生宛に送信：

```
大平先生

お疲れ様です。齋藤です。

本日（2026年__月__日）、以下の論文を Statistical Journal of the IAOS へ投稿いたしました。

タイトル：Known Censoring, Not Missingness: Cell Suppression and Partial Identification 
           in Open Administrative Healthcare Data
Manuscript ID：[取得後に記入]

つきましては、Sage の投稿システムから先生宛てに利益相反（COI）開示フォームのご記入依頼が
届きましたら、ご対応いただけますと幸いです。

どうぞよろしくお願いいたします。

齋藤
```

---

*このチェックリストは 2026-07-08 に作成。投稿前に全項目を確認すること。*

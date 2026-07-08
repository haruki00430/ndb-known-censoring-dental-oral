# Dental/Oral Full Extraction QC — Handoff Note for Codex

**QC Date**: 2026-07-07  
**Verdict**: **QC_PASS_TABLES_READY**

---

## 1. Count Reproduction

All reported counts were **reproduced from CSV/JSON files**.

| Metric | Reported | Computed | Status |
|--------|---------|---------|--------|
| Total cells (retained releases) | 71,017 | 71,017 | ✅ |
| Observed | 45,285 | 45,285 | ✅ |
| Suppressed | 25,732 | 25,732 | ✅ |
| Primary low-count | 4,982 | 4,982 | ✅ |
| Ambiguous suppressed | 20,750 | 20,750 | ✅ |
| Blank | 0 | 0 | ✅ |
| Parse errors | 0 | 0 | ✅ |

Discrepancies: **None**

---

## 2. Key QC Findings

- **No.8 exclusion**: Confirmed excluded from disease-count series (metric_change: 算定回数).
- **Rule variants**: All three variants (missing / aggressive / standard) correctly assigned.
- **Missing-rule releases (No.1–2)**: No primary bounds assigned. ✅
- **Standard-rule releases (No.5–11)**: Zero primary-bounded cells (n_supp always ≥ 2). ✅
- **Aggressive-rule releases (No.3–4)**: 4,982 primary-bounded cells [1, 9] only for rows with n_supp < 47. ✅
- **dental_bounds_primary.csv integrity**: 0 ambiguous cells; all entries count_lower=1, count_upper=9, lower_bound_rule=event_exists. ✅

**Anomaly documented**: No.3, row 'う蝕第３度歯髄壊死' (宮崎県) — n_supp=1 despite 46 non-zero observed cells,
inconsistent with aggressive complementary rule theory. Cell classified as primary_low_count [1,9].
Bounds remain defensible. Recommend footnote in manuscript Methods.

---

## 3. Manuscript Table Generation

Table generation **approved**. Files created:

  - manuscript_tables/table1_release_rule_inventory.csv
  - manuscript_tables/table1_release_rule_inventory.md
  - manuscript_tables/table2_observability_by_release.csv
  - manuscript_tables/table2_observability_by_release.md
  - manuscript_tables/table3_suppression_subtype_bounds.csv
  - manuscript_tables/table3_suppression_subtype_bounds.md
  - manuscript_tables/table4_naive_handling_strategies.csv
  - manuscript_tables/table4_naive_handling_strategies.md

---

## 4. Figure Data Generation

Figure data files created:

  - figure_data/figure1_rule_variant_timeline.csv
  - figure_data/figure2_observability_heatmap_data.csv
  - figure_data/figure3_bounds_eligibility_by_release.csv

---

## 5. Main-Text vs. Supplement Recommendation

| Item | Placement |
|------|-----------|
| Table 1: Release/rule inventory | **Main text** |
| Table 2: Observability by release | **Main text** |
| Table 3: Suppression subtype and bounds eligibility | **Main text** |
| Table 4: Naive handling strategies | **Main text or Supplement** (per journal length) |
| Figure 1 data: Rule variant timeline | **Main text** |
| Figure 2 data: Observability heatmap | **Main text** |
| Figure 3 data: Bounds eligibility by release | **Main text** |
| Full indicator catalog (`dental_indicator_catalog.csv`) | **Supplement** |
| Row-context distributions | **Supplement** |
| Detailed naive-handling readiness (`dental_naive_handling_ready.csv`) | **Supplement** |

---

## 6. Framing Note

> The public release identifies some suppressed cells as bounded observations,
> while other suppressed cells remain only partially characterized because of
> missing or complementary disclosure rules.

Use 'identification region' or 'bounds eligibility' — not 'imputed value'.

---

*Source of truth: CSV/JSON in `results/full_extraction/`. QC script: `scripts/qc_and_tables.py`.*
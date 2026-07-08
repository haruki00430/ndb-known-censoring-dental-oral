## Table 4. Naive Handling Strategies for Suppressed Cells

| Strategy | Treatment of suppressed cells | Applicable to all suppressed cells? | Main assumption | Main risk | Appropriate role in manuscript |
|---|---|---|---|---|---|
| Complete-case analysis | Exclude suppressed cells from analysis | Yes | Suppressed cells are missing at random | Systematic exclusion of low-count (typically rural or small-population) prefectures; introduces selection bias | Comparison benchmark; not recommended as primary analysis |
| Zero substitution | Assign count = 0 | Yes | Suppressed cells contain zero events | Directly contradicts disclosure rule: zero is published explicitly as 0, so suppressed cells must contain ≥ 1 event | Illustrative lower-bound scenario; logically inconsistent with disclosure mechanism |
| Upper-bound substitution | Assign count = T − 1 = 9 | Yes (primary); conservative for ambiguous | Suppressed cells contain the maximum possible value below T | Systematic overestimation, particularly for rare conditions | Conservative upper-bound sensitivity analysis |
| Midpoint substitution | Assign count = (1 + 9) / 2 = 5 | Only for primary low-count cells with verified [1, 9] bounds | Uniform distribution of true count within identification region [1, 9] | Uniform distribution is unjustified; overestimates cells near lower bound | Sensitivity analysis; not recommended for primary inference |

*All four strategies are implementable from `dental_naive_handling_ready.csv`. None of these strategies uses known-censoring partial identification. The manuscript compares each against the interval-based approach.*
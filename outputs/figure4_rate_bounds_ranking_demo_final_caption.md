# Figure 4 Caption

**Figure 4. Rate bounds and ranking support under known censoring in NDB Open Data Dental/Oral indicators.**

Panel A shows prefecture-level rate bounds per 100,000 population for two selected fiscal years (FY2016, No.3, aggressive suppression rule; FY2023, No.10, standard suppression rule) and two indicators (IND_5220077: hematogenous pulpitis [血行性歯髄炎]; IND_5210011: root canal filling completed [根充済み]).
Observed cells are shown as filled circles (point-identified).
Primary low-count suppressed cells (count ∈ [1, 9]) are shown as horizontal intervals derived from the public suppression rule: [1/population, 9/population] × 100,000.
Ambiguous suppression cells are shown as × marks and are not assigned numeric bounds.

Panel B shows the corresponding ranking support for the same set.
Stable point-identified ranks are shown as filled circles.
Interval-ranked cells (where primary bounds permit partial rank ordering) are shown as horizontal intervals indicating the range of possible ranks.
Cells with ambiguous suppression are excluded from numeric rank assignment (× marks).

Panel C compares four naive ranking strategies for hematogenous pulpitis (No.1/FY2014, missing suppression rule) as comparison benchmarks.
The strategies — complete case, zero substitution, upper-bound substitution (T-1), and midpoint imputation — are shown for all 47 prefectures.
**This panel is a benchmark only. None of these naive strategies constitute valid statistical inference, and the ranks they produce are not identified by the public release.**

*Rate and ranking analyses are identification exercises. They show which regional comparisons are supported by the public release and disclosure rule; they do not recover hidden suppressed counts.*

---

## Figure Reference Sentence (Results Section)

> Figure 4 demonstrates the partial identification framework at the prefecture level.
> Panel A shows that, under the aggressive suppression rule (FY2016, No.3), 46 of 47 prefectures for hematogenous pulpitis received interval-bounded rates rather than point estimates, because all suppressed cells were primary low-count and their counts were publicly constrained to [1, 9].
> Under the standard rule (FY2023, No.10), 45 of 47 prefectures were point-identified and 2 remained ambiguous.
> Panel B confirms that rank ordering follows the same pattern: in FY2016, 46 prefectures received rank intervals rather than stable point ranks.
> Panel C illustrates that naive substitution strategies for the missing-rule release (No.1/FY2014) produce divergent apparent rankings that are not identified by the public release.

---

## Limitation Note

> The prefecture-level rate and ranking analysis presented here uses the prefecture-level source data for selected indicators only.
> The aggregate-draft Figure 4 from the earlier manuscript module is superseded by this figure.

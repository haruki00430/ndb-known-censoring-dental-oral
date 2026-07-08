## Table 1. NDB Open Data Release Inventory and Disclosure Rule Variant

| NDB release | Fiscal year | Retained in disease-count series | File/metric label | Rule status | Rule variant | Suppression threshold | Primary-bounds eligibility | Notes |
|---|---|---|---|---|---|---|---|---|
| No.1 | 2014 | Yes | disease_count | missing | missing |  | no | No suppression rule text found in header |
| No.2 | 2015 | Yes | disease_count | missing | missing |  | no | No suppression rule text found in header |
| No.3 | 2016 | Yes | disease_count | verified | aggressive | 10 | yes | Complementary rule suppresses all 47 prefecture cells when 1 cell < T |
| No.4 | 2017 | Yes | disease_count | verified | aggressive | 10 | yes | Complementary rule suppresses all 47 prefecture cells when 1 cell < T |
| No.5 | 2018 | Yes | disease_count | verified | standard | 10 | yes | Complementary rule suppresses minimum cells ≥ T when 1 cell < T |
| No.6 | 2019 | Yes | disease_count | verified | standard | 10 | yes | Complementary rule suppresses minimum cells ≥ T when 1 cell < T |
| No.7 | 2020 | Yes | disease_count | verified | standard | 10 | yes | Complementary rule suppresses minimum cells ≥ T when 1 cell < T |
| No.8 | 2021 | No (excluded) | claim_count | verified | standard | 10 | yes | Excluded: metric label is 算定回数 (claim count), not 傷病件数 (disease count) |
| No.9 | 2022 | Yes | disease_count | verified | standard | 10 | yes | Complementary rule suppresses minimum cells ≥ T when 1 cell < T |
| No.10 | 2023 | Yes | disease_count | verified | standard | 10 | yes | Complementary rule suppresses minimum cells ≥ T; public-expense claims excluded from FY2023 |
| No.11 | 2024 | Yes | disease_count | verified | standard | 10 | yes | Complementary rule suppresses minimum cells ≥ T; public-expense claims excluded |

*T = suppression threshold; — = not applicable (rule text not present).*
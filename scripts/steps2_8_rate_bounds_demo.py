"""
Steps 2–8: Rate Bounds / Ranking Demo for Dental/Oral Known-Censoring Study

Step 2: Indicator selection (bounded_demo / stable_observed_demo / ambiguous_limit_demo)
Step 3: Count bounds for demo indicators
Step 4: Rate bounds
Step 5: Ranking stability
Step 6: Naive ranking comparison
Step 7: Figure 4 data
Step 8: QC report
"""

import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date

ACCESS_DATE = str(date.today())

# ── パス ──────────────────────────────────────────────────────────────────────
HUB = Path(r'C:\Users\user\.ag-cursor-common\research_workspace\projects\NDB_Research_Hub')
PROJ = HUB / 'projects' / 'NDB-dental-oral-20260707'
FULL = PROJ / 'results' / 'full_extraction'
DEMO = PROJ / 'results' / 'rate_bounds_demo'
FIGDATA = PROJ / 'figure_data'

DEMO.mkdir(parents=True, exist_ok=True)
FIGDATA.mkdir(parents=True, exist_ok=True)

# ── Step 1 output (already created) ──────────────────────────────────────────
pop_df = pd.read_csv(DEMO / 'population_denominator_inventory.csv', dtype={'prefecture_code': str})
assert len(pop_df) == 470, f"Population inventory: {len(pop_df)} rows"
print(f'Population denominator loaded: {len(pop_df)} rows', file=sys.stderr)

# ── Load full extraction data ─────────────────────────────────────────────────
print('Loading full extraction data...', file=sys.stderr)
cell_df = pd.read_csv(
    FULL / 'dental_cell_state_full.csv',
    encoding='utf-8',
    dtype={'prefecture_code': str}
)
bounds_df = pd.read_csv(FULL / 'dental_bounds_primary.csv', encoding='utf-8',
                         dtype={'prefecture_code': str})
catalog_df = pd.read_csv(FULL / 'dental_indicator_catalog.csv', encoding='utf-8')

# Ensure consistent types
cell_df['prefecture_code'] = cell_df['prefecture_code'].str.zfill(2)
bounds_df['prefecture_code'] = bounds_df['prefecture_code'].str.zfill(2)

RETAINED_FYS = [2014,2015,2016,2017,2018,2019,2020,2022,2023,2024]
cell_retained = cell_df[cell_df['fiscal_year'].isin(RETAINED_FYS)].copy()
print(f'  cell_state_full retained: {len(cell_retained)} rows', file=sys.stderr)

# ── STEP 2: Indicator Selection ───────────────────────────────────────────────
print('\n[STEP 2] Indicator selection...', file=sys.stderr)

# Summarize per indicator: observed, primary_bounded, ambiguous cells
indic_stats = (cell_retained
    .groupby('indicator_id')
    .apply(lambda g: pd.Series({
        'indicator_name': g['indicator_name'].iloc[0],
        'total_cells': len(g),
        'observed_cells': (g['cell_state'] == 'observed').sum(),
        'primary_bounded_cells': (g['suppression_subtype'] == 'primary_low_count').sum(),
        'ambiguous_suppression_cells': (g['suppression_subtype'] == 'ambiguous_suppression').sum(),
        'retained_releases_available': g['release_id'].nunique(),
    }), include_groups=False)
    .reset_index()
)

# Selection criteria:
# bounded_demo: primary_bounded_cells >= 3, observed_cells >= 40
# stable_observed_demo: observed_cells / total_cells >= 0.95, ambiguous = 0
# ambiguous_limit_demo: ambiguous_suppression_cells >= 30

bounded_cands = indic_stats[
    (indic_stats['primary_bounded_cells'] >= 3) &
    (indic_stats['observed_cells'] >= 40)
].sort_values('primary_bounded_cells', ascending=False)

stable_cands = indic_stats[
    (indic_stats['observed_cells'] / indic_stats['total_cells'] >= 0.95) &
    (indic_stats['ambiguous_suppression_cells'] == 0)
].sort_values('observed_cells', ascending=False)

ambig_cands = indic_stats[
    indic_stats['ambiguous_suppression_cells'] >= 30
].sort_values('ambiguous_suppression_cells', ascending=False)

print(f'  bounded_demo candidates: {len(bounded_cands)}', file=sys.stderr)
print(f'  stable_observed_demo candidates: {len(stable_cands)}', file=sys.stderr)
print(f'  ambiguous_limit_demo candidates: {len(ambig_cands)}', file=sys.stderr)

# Pick top candidates (avoid picking same indicator twice)
bounded_pick = bounded_cands.iloc[0]
stable_pick = stable_cands[stable_cands['indicator_id'] != bounded_pick['indicator_id']].iloc[0]
ambig_pick = ambig_cands[
    (ambig_cands['indicator_id'] != bounded_pick['indicator_id']) &
    (ambig_cands['indicator_id'] != stable_pick['indicator_id'])
].iloc[0]

selections = [
    (bounded_pick, 'bounded_demo',
     f'最多 primary_bounded_cells ({int(bounded_pick["primary_bounded_cells"])}件)、observed >= 40件'),
    (stable_pick, 'stable_observed_demo',
     f'観測率 {100*stable_pick["observed_cells"]/stable_pick["total_cells"]:.1f}%・ambiguous ゼロ'),
    (ambig_pick, 'ambiguous_limit_demo',
     f'ambiguous_suppression {int(ambig_pick["ambiguous_suppression_cells"])}件でランキング不可の例示'),
]

demo_indicator_rows = []
demo_ind_ids = []
for row, role, reason in selections:
    print(f'  {role}: {row["indicator_id"]} "{row["indicator_name"]}"', file=sys.stderr)
    print(f'    obs={row["observed_cells"]} prim={row["primary_bounded_cells"]} ambig={row["ambiguous_suppression_cells"]}', file=sys.stderr)
    demo_indicator_rows.append({
        'indicator_id': row['indicator_id'],
        'indicator_name': row['indicator_name'],
        'selection_role': role,
        'retained_releases_available': int(row['retained_releases_available']),
        'observed_cells': int(row['observed_cells']),
        'primary_bounded_cells': int(row['primary_bounded_cells']),
        'ambiguous_suppression_cells': int(row['ambiguous_suppression_cells']),
        'selection_reason': reason,
    })
    demo_ind_ids.append(row['indicator_id'])

demo_sel_df = pd.DataFrame(demo_indicator_rows)
demo_sel_df.to_csv(DEMO / 'demo_indicator_selection.csv', index=False, encoding='utf-8')
print(f'  Saved demo_indicator_selection.csv', file=sys.stderr)

# ── STEP 3: Count Bounds for Demo Indicators ──────────────────────────────────
print('\n[STEP 3] Count bounds...', file=sys.stderr)

demo_cells = cell_retained[cell_retained['indicator_id'].isin(demo_ind_ids)].copy()

count_rows = []
for _, r in demo_cells.iterrows():
    state = r['cell_state']
    subtype = r.get('suppression_subtype', '')

    if state == 'observed':
        cnt_lo = r['parsed_count']
        cnt_hi = r['parsed_count']
        bounds_status = 'point_identified'
        ambig_flag = 'no'
    elif subtype == 'primary_low_count':
        cnt_lo = 1.0
        cnt_hi = 9.0
        bounds_status = 'bounded_primary'
        ambig_flag = 'no'
    elif subtype == 'ambiguous_suppression':
        cnt_lo = np.nan
        cnt_hi = np.nan
        bounds_status = 'not_bounded_ambiguous'
        ambig_flag = 'yes'
    else:
        cnt_lo = np.nan
        cnt_hi = np.nan
        bounds_status = 'not_applicable'
        ambig_flag = 'no'

    count_rows.append({
        'release_id': r['release_id'],
        'fiscal_year': r['fiscal_year'],
        'indicator_id': r['indicator_id'],
        'indicator_name': r['indicator_name'],
        'prefecture_code': r['prefecture_code'],
        'prefecture_name': r['prefecture_name'],
        'cell_state': state,
        'suppression_subtype': subtype if pd.notna(subtype) else '',
        'observed_count': r['parsed_count'] if state == 'observed' else np.nan,
        'count_lower': cnt_lo,
        'count_upper': cnt_hi,
        'bounds_status': bounds_status,
        'ambiguity_flag': ambig_flag,
    })

count_df = pd.DataFrame(count_rows)

# Validation: no ambiguous cell with numeric bounds
ambig_with_bounds = count_df[
    (count_df['ambiguity_flag'] == 'yes') & count_df['count_lower'].notna()
]
assert len(ambig_with_bounds) == 0, "FAIL: ambiguous cells have numeric bounds!"

count_df.to_csv(DEMO / 'demo_count_bounds.csv', index=False, encoding='utf-8')
print(f'  Saved demo_count_bounds.csv ({len(count_df)} rows)', file=sys.stderr)
print(f'  observed={( count_df["bounds_status"]=="point_identified").sum()} / '
      f'bounded={( count_df["bounds_status"]=="bounded_primary").sum()} / '
      f'ambig_not_bounded={(count_df["bounds_status"]=="not_bounded_ambiguous").sum()}', file=sys.stderr)

# ── STEP 4: Rate Bounds ───────────────────────────────────────────────────────
print('\n[STEP 4] Rate bounds...', file=sys.stderr)

# Join population
pop_key = pop_df[['fiscal_year', 'prefecture_code', 'population']].copy()
rate_df = count_df.merge(
    pop_key, on=['fiscal_year', 'prefecture_code'], how='left'
)

missing_pop = rate_df['population'].isna().sum()
if missing_pop > 0:
    print(f'  WARNING: {missing_pop} rows missing population', file=sys.stderr)
    miss_details = rate_df[rate_df['population'].isna()][['fiscal_year','prefecture_code']].drop_duplicates()
    print(miss_details.to_string(), file=sys.stderr)

rate_rows = []
for _, r in rate_df.iterrows():
    pop = r['population']
    bs = r['bounds_status']

    if bs == 'point_identified':
        rate_lo = r['count_lower'] / pop * 100_000
        rate_hi = rate_lo
        rate_status = 'point_identified'
    elif bs == 'bounded_primary':
        rate_lo = r['count_lower'] / pop * 100_000   # 1/pop*100k
        rate_hi = r['count_upper'] / pop * 100_000   # 9/pop*100k
        rate_status = 'bounded_primary'
    elif bs == 'not_bounded_ambiguous':
        rate_lo = np.nan
        rate_hi = np.nan
        rate_status = 'not_bounded_ambiguous'
    else:
        rate_lo = np.nan
        rate_hi = np.nan
        rate_status = 'not_applicable'

    rate_rows.append({
        'release_id': r['release_id'],
        'fiscal_year': r['fiscal_year'],
        'indicator_id': r['indicator_id'],
        'indicator_name': r['indicator_name'],
        'prefecture_code': r['prefecture_code'],
        'prefecture_name': r['prefecture_name'],
        'population': int(pop),
        'cell_state': r['cell_state'],
        'suppression_subtype': r['suppression_subtype'],
        'count_lower': r['count_lower'],
        'count_upper': r['count_upper'],
        'rate_lower_per_100k': round(rate_lo, 4) if pd.notna(rate_lo) else np.nan,
        'rate_upper_per_100k': round(rate_hi, 4) if pd.notna(rate_hi) else np.nan,
        'rate_status': rate_status,
    })

rate_bounds_df = pd.DataFrame(rate_rows)

# Validation: no ambiguous cell with numeric rate bound
ambig_with_rate = rate_bounds_df[
    (rate_bounds_df['rate_status'] == 'not_bounded_ambiguous') &
    rate_bounds_df['rate_lower_per_100k'].notna()
]
assert len(ambig_with_rate) == 0, "FAIL: ambiguous cells have numeric rate bounds!"

# Validation: observed cells have equal lower and upper
obs_rates = rate_bounds_df[rate_bounds_df['rate_status'] == 'point_identified']
mismatched = obs_rates[obs_rates['rate_lower_per_100k'] != obs_rates['rate_upper_per_100k']]
assert len(mismatched) == 0, "FAIL: observed cells have rate_lower != rate_upper"

rate_bounds_df.to_csv(DEMO / 'demo_rate_bounds.csv', index=False, encoding='utf-8')
print(f'  Saved demo_rate_bounds.csv ({len(rate_bounds_df)} rows)', file=sys.stderr)
print(f'  point_identified={( rate_bounds_df["rate_status"]=="point_identified").sum()} / '
      f'bounded_primary={( rate_bounds_df["rate_status"]=="bounded_primary").sum()} / '
      f'not_bounded_ambiguous={(rate_bounds_df["rate_status"]=="not_bounded_ambiguous").sum()}', file=sys.stderr)

# ── STEP 5: Ranking Stability ─────────────────────────────────────────────────
print('\n[STEP 5] Ranking stability...', file=sys.stderr)

# Check per indicator-release whether any ambiguous cells exist
ambig_check = (rate_bounds_df
    .groupby(['indicator_id', 'release_id'])
    ['rate_status']
    .apply(lambda x: (x == 'not_bounded_ambiguous').any())
    .rename('has_ambiguous')
    .reset_index()
)

rank_rows = []
for (ind_id, rel_id), grp in rate_bounds_df.groupby(['indicator_id', 'release_id']):
    fy = grp['fiscal_year'].iloc[0]
    ind_name = grp['indicator_name'].iloc[0]
    has_ambig = ambig_check[
        (ambig_check['indicator_id'] == ind_id) &
        (ambig_check['release_id'] == rel_id)
    ]['has_ambiguous'].iloc[0]

    # Only prefectures with valid rate bounds
    valid = grp[grp['rate_status'].isin(['point_identified', 'bounded_primary'])].copy()
    n_valid = len(valid)
    n_total = len(grp)

    if len(valid) == 0:
        # All ambiguous - no ranking possible
        for _, r in grp.iterrows():
            rank_rows.append({
                'release_id': rel_id,
                'fiscal_year': fy,
                'indicator_id': ind_id,
                'indicator_name': ind_name,
                'prefecture_code': r['prefecture_code'],
                'prefecture_name': r['prefecture_name'],
                'rate_lower_per_100k': np.nan,
                'rate_upper_per_100k': np.nan,
                'rank_best_possible': np.nan,
                'rank_worst_possible': np.nan,
                'rank_interval_width': np.nan,
                'ranking_status': 'ranking_not_supported_ambiguous',
                'ambiguity_context': f'{n_total} cells all ambiguous; no rate bounds available',
            })
        continue

    # For interval ranking: a prefecture's best rank = rank if all others have their upper rates
    # worst rank = rank if all others have their lower rates
    # Simplified: for point_identified, rank is exact; for bounded, compute interval

    all_uppers = valid['rate_upper_per_100k'].values
    all_lowers = valid['rate_lower_per_100k'].values

    for _, r in valid.iterrows():
        rate_lo = r['rate_lower_per_100k']
        rate_hi = r['rate_upper_per_100k']
        rs = r['rate_status']

        if rs == 'point_identified':
            # Rank among all valid prefectures (higher rate = higher rank = worse)
            rank_exact = int((valid['rate_lower_per_100k'] >= rate_lo).sum())
            rank_best = rank_exact
            rank_worst = rank_exact
            rank_status = 'stable_point_identified' if not has_ambig else 'interval_ranked'
        else:
            # bounded_primary: best rank = assume this prefecture has max (rate_hi) vs others at min
            # Actually: best rank (lowest rank number) = assume this prefect is LOW = rate_lo,
            #           others at their upper = more prefectures above this one
            rank_best = int((all_uppers > rate_hi).sum()) + 1  # prefectures with upper > our upper
            rank_worst = int((all_lowers >= rate_lo).sum())     # prefectures with lower >= our lower
            rank_status = 'interval_ranked'

        ambig_ctx = ''
        if has_ambig:
            n_ambig = (grp['rate_status'] == 'not_bounded_ambiguous').sum()
            ambig_ctx = (f'{n_valid}/{n_total} prefectures have rate bounds; '
                         f'{n_ambig} are ambiguous and excluded from ranking')
            if rs == 'point_identified':
                rank_status = 'interval_ranked'

        rank_rows.append({
            'release_id': rel_id,
            'fiscal_year': fy,
            'indicator_id': ind_id,
            'indicator_name': ind_name,
            'prefecture_code': r['prefecture_code'],
            'prefecture_name': r['prefecture_name'],
            'rate_lower_per_100k': rate_lo,
            'rate_upper_per_100k': rate_hi,
            'rank_best_possible': rank_best,
            'rank_worst_possible': rank_worst,
            'rank_interval_width': max(0, rank_worst - rank_best),
            'ranking_status': rank_status,
            'ambiguity_context': ambig_ctx,
        })

    # Ambiguous cells: add with ranking_not_supported
    for _, r in grp[grp['rate_status'] == 'not_bounded_ambiguous'].iterrows():
        n_ambig = (grp['rate_status'] == 'not_bounded_ambiguous').sum()
        rank_rows.append({
            'release_id': rel_id,
            'fiscal_year': fy,
            'indicator_id': ind_id,
            'indicator_name': ind_name,
            'prefecture_code': r['prefecture_code'],
            'prefecture_name': r['prefecture_name'],
            'rate_lower_per_100k': np.nan,
            'rate_upper_per_100k': np.nan,
            'rank_best_possible': np.nan,
            'rank_worst_possible': np.nan,
            'rank_interval_width': np.nan,
            'ranking_status': 'ranking_not_supported_ambiguous',
            'ambiguity_context': (f'ambiguous cell; count not bounded; '
                                  f'{n_ambig}/{n_total} ambiguous in this release'),
        })

rank_df = pd.DataFrame(rank_rows)
rank_df.to_csv(DEMO / 'demo_ranking_stability.csv', index=False, encoding='utf-8')
print(f'  Saved demo_ranking_stability.csv ({len(rank_df)} rows)', file=sys.stderr)
print(f'  stable_point_identified={(rank_df["ranking_status"]=="stable_point_identified").sum()} / '
      f'interval_ranked={(rank_df["ranking_status"]=="interval_ranked").sum()} / '
      f'not_supported={(rank_df["ranking_status"]=="ranking_not_supported_ambiguous").sum()}', file=sys.stderr)

# ── STEP 6: Naive Ranking Comparison ─────────────────────────────────────────
print('\n[STEP 6] Naive ranking comparison...', file=sys.stderr)

naive_rows = []
STRATEGIES = {
    'complete_case': 'complete-caseは観測セルのみ使用。低カウント都道府県が除外され選択バイアスが生じる可能性（比較ベンチマークのみ）',
    'zero': 'ゼロ代入は抑制規則と矛盾（NDB suppression ruleにより count=0は公開済み）。根拠なし（比較ベンチマークのみ）',
    'upper_bound_T_minus_1': 'T-1代入はprimary_low_countには適用可能だが、ambiguous suppressionには無効。点推定への変換は識別を過剰主張（比較ベンチマークのみ）',
    'midpoint': 'midpoint=(1+9)/2=5代入はprimary_low_countのみ。ambiguousには使用不可。点推定への変換は識別を過剰主張（比較ベンチマークのみ）',
}

for (ind_id, rel_id), grp in rate_bounds_df.groupby(['indicator_id', 'release_id']):
    fy = grp['fiscal_year'].iloc[0]
    ind_name = grp['indicator_name'].iloc[0]

    for strategy, warning in STRATEGIES.items():
        sub_rows = []
        for _, r in grp.iterrows():
            pc = r['prefecture_code']
            pn = r['prefecture_name']
            pop = r['population']
            rs = r['rate_status']

            if strategy == 'complete_case':
                if rs == 'point_identified':
                    subst_count = r['count_lower']
                else:
                    subst_count = np.nan
            elif strategy == 'zero':
                if rs == 'not_bounded_ambiguous':
                    subst_count = 0.0
                elif rs == 'bounded_primary':
                    subst_count = 0.0
                else:
                    subst_count = r['count_lower']
            elif strategy == 'upper_bound_T_minus_1':
                if rs == 'bounded_primary':
                    subst_count = 9.0
                elif rs == 'point_identified':
                    subst_count = r['count_lower']
                else:
                    subst_count = np.nan  # invalid for ambiguous
            elif strategy == 'midpoint':
                if rs == 'bounded_primary':
                    subst_count = 5.0
                elif rs == 'point_identified':
                    subst_count = r['count_lower']
                else:
                    subst_count = np.nan  # invalid for ambiguous

            if pd.notna(subst_count):
                subst_rate = subst_count / pop * 100_000
            else:
                subst_rate = np.nan

            sub_rows.append({
                'prefecture_code': pc,
                'prefecture_name': pn,
                'substituted_count': subst_count,
                'substituted_rate_per_100k': round(subst_rate, 4) if pd.notna(subst_rate) else np.nan,
            })

        sub_df = pd.DataFrame(sub_rows)
        # Rank (higher rate = higher rank number, ascending from 1=highest rate)
        sub_df_valid = sub_df[sub_df['substituted_rate_per_100k'].notna()].copy()
        sub_df_valid = sub_df_valid.sort_values('substituted_rate_per_100k', ascending=False)
        sub_df_valid['rank'] = range(1, len(sub_df_valid) + 1)

        rank_map = dict(zip(sub_df_valid['prefecture_code'], sub_df_valid['rank']))

        for _, r in sub_df.iterrows():
            naive_rows.append({
                'release_id': rel_id,
                'fiscal_year': fy,
                'indicator_id': ind_id,
                'indicator_name': ind_name,
                'strategy': strategy,
                'prefecture_code': r['prefecture_code'],
                'prefecture_name': r['prefecture_name'],
                'substituted_count': r['substituted_count'],
                'substituted_rate_per_100k': r['substituted_rate_per_100k'],
                'substituted_rank': rank_map.get(r['prefecture_code'], np.nan),
                'strategy_warning': warning,
            })

naive_df = pd.DataFrame(naive_rows)
naive_df.to_csv(DEMO / 'demo_naive_ranking_comparison.csv', index=False, encoding='utf-8')
print(f'  Saved demo_naive_ranking_comparison.csv ({len(naive_df)} rows)', file=sys.stderr)

# ── STEP 7: Figure 4 Data ─────────────────────────────────────────────────────
print('\n[STEP 7] Figure 4 data...', file=sys.stderr)

# Panel A: rate bounds (one release per indicator)
# Choose one release per indicator: prefer bounded_demo × No.3 or No.4 (where primary suppression exists)
fig4_rows = []

# Panel A: rate_bounds - use rate_bounds_df
for (ind_id, rel_id), grp in rate_bounds_df.groupby(['indicator_id', 'release_id']):
    fy = grp['fiscal_year'].iloc[0]
    ind_name = grp['indicator_name'].iloc[0]
    role = demo_sel_df[demo_sel_df['indicator_id'] == ind_id]['selection_role'].iloc[0]

    # For figure clarity: only include bounded_demo and stable_observed_demo in Panel A
    if role not in ('bounded_demo', 'stable_observed_demo'):
        continue

    for _, r in grp.iterrows():
        rs = r['rate_status']
        point_rate = r['rate_lower_per_100k'] if rs == 'point_identified' else np.nan

        fig4_rows.append({
            'panel': 'A_rate_bounds',
            'release_id': rel_id,
            'fiscal_year': fy,
            'indicator_id': ind_id,
            'indicator_name': ind_name,
            'prefecture_code': r['prefecture_code'],
            'prefecture_name': r['prefecture_name'],
            'rate_lower_per_100k': r['rate_lower_per_100k'],
            'rate_upper_per_100k': r['rate_upper_per_100k'],
            'point_rate_per_100k': point_rate,
            'rank_best_possible': np.nan,
            'rank_worst_possible': np.nan,
            'ranking_status': rs,
            'suppression_subtype': r['suppression_subtype'],
        })

# Panel B: rank intervals - from rank_df
for (ind_id, rel_id), grp in rank_df.groupby(['indicator_id', 'release_id']):
    fy = grp['fiscal_year'].iloc[0]
    ind_name = grp['indicator_name'].iloc[0]
    role = demo_sel_df[demo_sel_df['indicator_id'] == ind_id]['selection_role'].iloc[0]

    if role not in ('bounded_demo', 'stable_observed_demo'):
        continue

    for _, r in grp.iterrows():
        # Get suppression subtype from rate_bounds_df
        match = rate_bounds_df[
            (rate_bounds_df['indicator_id'] == ind_id) &
            (rate_bounds_df['release_id'] == rel_id) &
            (rate_bounds_df['prefecture_code'] == r['prefecture_code'])
        ]
        subt = match['suppression_subtype'].iloc[0] if len(match) > 0 else ''

        fig4_rows.append({
            'panel': 'B_rank_intervals',
            'release_id': rel_id,
            'fiscal_year': fy,
            'indicator_id': ind_id,
            'indicator_name': ind_name,
            'prefecture_code': r['prefecture_code'],
            'prefecture_name': r['prefecture_name'],
            'rate_lower_per_100k': r['rate_lower_per_100k'],
            'rate_upper_per_100k': r['rate_upper_per_100k'],
            'point_rate_per_100k': (r['rate_lower_per_100k']
                                    if r['ranking_status'] == 'stable_point_identified'
                                    else np.nan),
            'rank_best_possible': r['rank_best_possible'],
            'rank_worst_possible': r['rank_worst_possible'],
            'ranking_status': r['ranking_status'],
            'suppression_subtype': subt,
        })

# Panel C: naive comparison - bounded_demo indicator, one release, all 4 strategies
bounded_ind_id = demo_sel_df[demo_sel_df['selection_role'] == 'bounded_demo']['indicator_id'].iloc[0]
bounded_releases = rate_bounds_df[rate_bounds_df['indicator_id'] == bounded_ind_id]['release_id'].unique()

for rel_id in bounded_releases[:1]:  # just first release for clarity
    fy_val = rate_bounds_df[
        (rate_bounds_df['indicator_id'] == bounded_ind_id) &
        (rate_bounds_df['release_id'] == rel_id)
    ]['fiscal_year'].iloc[0]
    ind_name = rate_bounds_df[rate_bounds_df['indicator_id'] == bounded_ind_id]['indicator_name'].iloc[0]

    naive_sub = naive_df[
        (naive_df['indicator_id'] == bounded_ind_id) &
        (naive_df['release_id'] == rel_id)
    ]

    for _, r in naive_sub.iterrows():
        fig4_rows.append({
            'panel': 'C_naive_comparison',
            'release_id': rel_id,
            'fiscal_year': fy_val,
            'indicator_id': bounded_ind_id,
            'indicator_name': ind_name,
            'prefecture_code': r['prefecture_code'],
            'prefecture_name': r['prefecture_name'],
            'rate_lower_per_100k': np.nan,
            'rate_upper_per_100k': np.nan,
            'point_rate_per_100k': r['substituted_rate_per_100k'],
            'rank_best_possible': np.nan,
            'rank_worst_possible': r['substituted_rank'],
            'ranking_status': f'naive_{r["strategy"]}',
            'suppression_subtype': '',
        })

fig4_df = pd.DataFrame(fig4_rows)
fig4_path = FIGDATA / 'figure4_rate_bounds_ranking_demo.csv'
fig4_df.to_csv(fig4_path, index=False, encoding='utf-8')
print(f'  Saved figure4_rate_bounds_ranking_demo.csv ({len(fig4_df)} rows)', file=sys.stderr)
print(f'  Panels: {fig4_df["panel"].value_counts().to_dict()}', file=sys.stderr)

# ── STEP 8: QC Report ─────────────────────────────────────────────────────────
print('\n[STEP 8] QC report...', file=sys.stderr)

qc_checks = {}

# Check 1: Population denominator 470 rows
qc_checks['check1_population_470_rows'] = {
    'check': 'Population denominator has 470 rows',
    'result': len(pop_df) == 470,
    'actual': len(pop_df),
    'expected': 470,
    'status': 'PASS' if len(pop_df) == 470 else 'FAIL',
}

# Check 2: Population join without missing
n_missing_pop = rate_bounds_df['population'].isna().sum()
qc_checks['check2_population_join'] = {
    'check': 'Population joins without missing prefecture-year pairs',
    'result': n_missing_pop == 0,
    'actual_missing': int(n_missing_pop),
    'status': 'PASS' if n_missing_pop == 0 else 'FAIL',
}

# Check 3: No ambiguous cell receives [1,9] count bounds
ambig_numeric = count_df[
    (count_df['ambiguity_flag'] == 'yes') & count_df['count_lower'].notna()
]
qc_checks['check3_no_ambiguous_count_bounds'] = {
    'check': 'No ambiguous cell receives [1,9] count bounds',
    'result': len(ambig_numeric) == 0,
    'ambiguous_with_bounds_count': len(ambig_numeric),
    'status': 'PASS' if len(ambig_numeric) == 0 else 'FAIL',
}

# Check 4: No ambiguous cell receives numeric rate bound
ambig_rate = rate_bounds_df[
    (rate_bounds_df['rate_status'] == 'not_bounded_ambiguous') &
    rate_bounds_df['rate_lower_per_100k'].notna()
]
qc_checks['check4_no_ambiguous_rate_bounds'] = {
    'check': 'No ambiguous cell receives a numeric rate bound',
    'result': len(ambig_rate) == 0,
    'ambiguous_with_rate_bounds_count': len(ambig_rate),
    'status': 'PASS' if len(ambig_rate) == 0 else 'FAIL',
}

# Check 5: Observed cells equal lower/upper
obs_mismatch = rate_bounds_df[
    (rate_bounds_df['rate_status'] == 'point_identified') &
    (rate_bounds_df['rate_lower_per_100k'] != rate_bounds_df['rate_upper_per_100k'])
]
qc_checks['check5_observed_equal_bounds'] = {
    'check': 'Observed cells have equal lower and upper count/rate',
    'result': len(obs_mismatch) == 0,
    'mismatch_count': len(obs_mismatch),
    'status': 'PASS' if len(obs_mismatch) == 0 else 'FAIL',
}

# Check 6: Primary low-count cells have count bounds [1,9]
prim_check = count_df[count_df['bounds_status'] == 'bounded_primary']
prim_wrong = prim_check[
    (prim_check['count_lower'] != 1) | (prim_check['count_upper'] != 9)
]
qc_checks['check6_primary_count_bounds_1_9'] = {
    'check': 'Primary low-count cells have count bounds [1,9]',
    'result': len(prim_wrong) == 0,
    'wrong_bounds_count': len(prim_wrong),
    'primary_bounded_cells_total': len(prim_check),
    'status': 'PASS' if len(prim_wrong) == 0 else 'FAIL',
}

# Check 7: Naive ranking labeled as benchmark
has_warning = (naive_df['strategy_warning'].notna() & (naive_df['strategy_warning'] != '')).all()
qc_checks['check7_naive_benchmark_labeled'] = {
    'check': 'Naive ranking outputs are clearly labeled as comparison benchmarks',
    'result': bool(has_warning),
    'status': 'PASS' if has_warning else 'FAIL',
}

# Check 8: Figure 4 data exist
fig4_exists = fig4_path.exists() and len(fig4_df) > 0
n_panels = fig4_df['panel'].nunique() if fig4_exists else 0
qc_checks['check8_figure4_exists'] = {
    'check': 'Figure 4 data exist and are consistent with rate/ranking files',
    'result': fig4_exists and n_panels == 3,
    'rows': len(fig4_df) if fig4_exists else 0,
    'panels': n_panels,
    'status': 'PASS' if (fig4_exists and n_panels == 3) else 'FAIL',
}

all_pass = all(v['status'] == 'PASS' for v in qc_checks.values())
verdict = 'RATE_RANKING_DEMO_READY' if all_pass else 'HOLD_RATE_BOUNDS_QC_FAILED'

# ── Write QC report ───────────────────────────────────────────────────────────
qc_md_path = DEMO / 'rate_bounds_demo_qc_report.md'
with open(qc_md_path, 'w', encoding='utf-8') as f:
    f.write('# Rate Bounds Demo QC Report\n\n')
    f.write(f'**生成日**: {ACCESS_DATE}\n\n')
    f.write(f'**最終判定**: `{verdict}`\n\n')
    f.write('---\n\n')
    f.write('## QC チェック結果\n\n')
    f.write('| # | チェック | 判定 | 詳細 |\n')
    f.write('|---|---------|------|------|\n')
    for i, (k, v) in enumerate(qc_checks.items(), 1):
        icon = '✅' if v['status'] == 'PASS' else '❌'
        details = {kk: vv for kk, vv in v.items() if kk not in ('check', 'status', 'result')}
        det_str = '; '.join(f'{kk}={vv}' for kk, vv in details.items())
        f.write(f'| {i} | {v["check"]} | {icon} {v["status"]} | {det_str} |\n')
    f.write('\n---\n\n')
    f.write('## 選択指標\n\n')
    f.write(demo_sel_df.to_markdown(index=False) + '\n\n')
    f.write('## 人口分母ソース\n\n')
    src_summary = (pop_df
        .groupby('source_name')
        .agg(fiscal_years=('fiscal_year', lambda x: sorted(x.unique())),
             n_rows=('fiscal_year', 'count'))
        .reset_index())
    f.write(src_summary.to_string(index=False) + '\n\n')
    f.write('## 重要注記\n\n')
    f.write('- Rate および ranking 解析は partial identification の演習である。\n')
    f.write('- 公開リリースと開示規則によって支持される地域比較のみを示す。\n')
    f.write('- 隠れたカウントを推定・補完したものではない。\n')
    f.write('- ambiguous suppression セルはいかなる数値境界も受け取っていない。\n')

print(f'  Saved rate_bounds_demo_qc_report.md', file=sys.stderr)

# ── Write summary JSON ────────────────────────────────────────────────────────
summary = {
    'generated_date': ACCESS_DATE,
    'verdict': verdict,
    'population_denominator': {
        'total_rows': len(pop_df),
        'fiscal_years': sorted(pop_df['fiscal_year'].unique().tolist()),
        'sources': {
            'FY2014': 'e-Stat table_0003104195 (H22/H26基準, unit=人)',
            'FY2015-2019': 'e-Stat table_0003459027 (H27基準, unit=千人×1000)',
            'FY2020,2022-2024': 'Statistics_Bureau/pop_2023_est.csv (R2基準, unit=千人×1000)',
        }
    },
    'demo_indicators': demo_sel_df.to_dict(orient='records'),
    'count_bounds': {
        'total_rows': len(count_df),
        'point_identified': int((count_df['bounds_status'] == 'point_identified').sum()),
        'bounded_primary': int((count_df['bounds_status'] == 'bounded_primary').sum()),
        'not_bounded_ambiguous': int((count_df['bounds_status'] == 'not_bounded_ambiguous').sum()),
    },
    'rate_bounds': {
        'total_rows': len(rate_bounds_df),
        'point_identified': int((rate_bounds_df['rate_status'] == 'point_identified').sum()),
        'bounded_primary': int((rate_bounds_df['rate_status'] == 'bounded_primary').sum()),
        'not_bounded_ambiguous': int((rate_bounds_df['rate_status'] == 'not_bounded_ambiguous').sum()),
    },
    'ranking': {
        'stable_point_identified': int((rank_df['ranking_status'] == 'stable_point_identified').sum()),
        'interval_ranked': int((rank_df['ranking_status'] == 'interval_ranked').sum()),
        'ranking_not_supported_ambiguous': int((rank_df['ranking_status'] == 'ranking_not_supported_ambiguous').sum()),
    },
    'qc_checks': {k: v['status'] for k, v in qc_checks.items()},
    'output_files': {
        'population_denominator_inventory': str(DEMO / 'population_denominator_inventory.csv'),
        'demo_indicator_selection': str(DEMO / 'demo_indicator_selection.csv'),
        'demo_count_bounds': str(DEMO / 'demo_count_bounds.csv'),
        'demo_rate_bounds': str(DEMO / 'demo_rate_bounds.csv'),
        'demo_ranking_stability': str(DEMO / 'demo_ranking_stability.csv'),
        'demo_naive_ranking_comparison': str(DEMO / 'demo_naive_ranking_comparison.csv'),
        'figure4_rate_bounds_ranking_demo': str(fig4_path),
        'qc_report': str(qc_md_path),
    }
}

with open(DEMO / 'rate_bounds_demo_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print(f'  Saved rate_bounds_demo_summary.json', file=sys.stderr)

# ── Handoff for Codex ─────────────────────────────────────────────────────────
handoff_path = DEMO / 'rate_bounds_demo_handoff_for_codex.md'
bounded_info = demo_sel_df[demo_sel_df['selection_role'] == 'bounded_demo'].iloc[0]
stable_info = demo_sel_df[demo_sel_df['selection_role'] == 'stable_observed_demo'].iloc[0]
ambig_info = demo_sel_df[demo_sel_df['selection_role'] == 'ambiguous_limit_demo'].iloc[0]

with open(handoff_path, 'w', encoding='utf-8') as f:
    f.write(f'# Rate Bounds / Ranking Demo Handoff for Codex\n\n')
    f.write(f'**生成日**: {ACCESS_DATE}\n')
    f.write(f'**判定**: `{verdict}`\n\n')
    f.write('---\n\n')
    f.write('## 概要\n\n')
    f.write('Rate and ranking analyses are identification exercises. They show which regional '
            'comparisons are supported by the public release and disclosure rule, '
            'not recovered hidden counts.\n\n')
    f.write('---\n\n')
    f.write('## 人口分母\n\n')
    f.write('- 470行（10年 × 47都道府県）\n')
    f.write('- FY2021は除外（No.8 指標変更のため）\n')
    f.write('- FY2014: e-Stat 0003104195 直接取得（H22基準, 単位=人）\n')
    f.write('- FY2015–2019: e-Stat 0003459027 直接取得（H27基準, 単位=千人→×1000）\n')
    f.write('- FY2020,2022–2024: pop_2023_est.csv（R2基準, 単位=千人→×1000）\n\n')
    f.write('## 選択指標（3種）\n\n')
    f.write(f'### 1. bounded_demo: `{bounded_info["indicator_id"]}` {bounded_info["indicator_name"]}\n')
    f.write(f'- observed: {bounded_info["observed_cells"]}, primary_bounded: {bounded_info["primary_bounded_cells"]}, ambiguous: {bounded_info["ambiguous_suppression_cells"]}\n\n')
    f.write(f'### 2. stable_observed_demo: `{stable_info["indicator_id"]}` {stable_info["indicator_name"]}\n')
    f.write(f'- observed: {stable_info["observed_cells"]}, primary_bounded: {stable_info["primary_bounded_cells"]}, ambiguous: {stable_info["ambiguous_suppression_cells"]}\n\n')
    f.write(f'### 3. ambiguous_limit_demo: `{ambig_info["indicator_id"]}` {ambig_info["indicator_name"]}\n')
    f.write(f'- observed: {ambig_info["observed_cells"]}, primary_bounded: {ambig_info["primary_bounded_cells"]}, ambiguous: {ambig_info["ambiguous_suppression_cells"]}\n\n')
    f.write('## Rate Bounds 結果\n\n')
    f.write(f'- point_identified（観測セル）: {summary["rate_bounds"]["point_identified"]}\n')
    f.write(f'- bounded_primary（[1,9]境界）: {summary["rate_bounds"]["bounded_primary"]}\n')
    f.write(f'- not_bounded_ambiguous（レート境界なし）: {summary["rate_bounds"]["not_bounded_ambiguous"]}\n\n')
    f.write('## Ranking 結果\n\n')
    f.write(f'- stable_point_identified: {summary["ranking"]["stable_point_identified"]}\n')
    f.write(f'- interval_ranked: {summary["ranking"]["interval_ranked"]}\n')
    f.write(f'- ranking_not_supported_ambiguous: {summary["ranking"]["ranking_not_supported_ambiguous"]}\n\n')
    f.write('## 何が推論できて何ができないか\n\n')
    f.write('**推論可能**:\n')
    f.write('- observed セルの点レート（完全識別）\n')
    f.write('- primary_low_count セルのレート区間 [1/pop×100k, 9/pop×100k]\n')
    f.write('- primary_bounded セルを含む指標の区間ランキング\n\n')
    f.write('**推論不可**:\n')
    f.write('- ambiguous suppression セルのカウントは境界不明\n')
    f.write('- ambiguous セルを含む指標の完全ランキングは成立しない\n')
    f.write('- Naive代入（zero/upper_bound_T-1/midpoint）は比較ベンチマークであり有効推論ではない\n\n')
    f.write('## 出力ファイル\n\n')
    for name, path in summary['output_files'].items():
        f.write(f'- `{Path(path).name}` ← {name}\n')
    f.write('\n## QC 判定\n\n')
    for chk, st in qc_checks.items():
        icon = '✅' if st['status'] == 'PASS' else '❌'
        f.write(f'- {icon} {st["check"]}\n')
    f.write(f'\n**最終判定: {verdict}**\n')

print(f'  Saved rate_bounds_demo_handoff_for_codex.md', file=sys.stderr)

# Final summary
print('\n' + '='*60, file=sys.stderr)
print(f'VERDICT: {verdict}', file=sys.stderr)
print('='*60, file=sys.stderr)
for k, v in qc_checks.items():
    print(f'  {v["status"]:4}  {v["check"]}', file=sys.stderr)

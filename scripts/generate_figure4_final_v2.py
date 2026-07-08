# -*- coding: utf-8 -*-
"""
generate_figure4_final_v2.py
============================
Generate Figure 1 (main demonstration figure) for the Known Censoring study.
All labels in English; prefecture names romanised; 300 dpi PNG + SVG output.

論文 Figure 1（レート境界・順位デモ）生成スクリプト v2
全ラベルを英語表記、都道府県名をローマ字表記、300 dpi PNG + SVG を出力する。

Panels / パネル:
  Panel A (3 columns): Prefecture-level rate bounds per 100,000 population
                       都道府県別レート境界（人口 10 万人あたり）
  Panel B (3 columns): Prefecture-level rank intervals
                       都道府県別ランク区間
  Panel C (full width): Naive ranking strategy comparison [BENCHMARK ONLY]
                        Naive ランキング戦略比較（ベンチマークのみ）

Input / 入力:
  figure_data/figure4_rate_bounds_ranking_demo.csv   (2,068 rows / 行)
  results/rate_bounds_demo/demo_naive_ranking_comparison.csv

Output / 出力:
  outputs/figure4_rate_bounds_ranking_demo_final_v2.png  (300 dpi)
  outputs/figure4_rate_bounds_ranking_demo_final_v2.svg

Usage / 実行方法:
  python scripts/generate_figure4_final_v2.py

Changes from v1 / v1 からの変更:
  - All text/labels in English / 全ラベルを英語化
  - Prefecture names romanised on y-axis / 都道府県名をローマ字に変更
  - Panel C: No.3/FY2016 data (divergent strategies visible) / No.3/FY2016 データに変更
  - Panel C: dot-plot with connecting lines / ドットプロット＋接続線に変更
  - Hokkaido at top → Okinawa at bottom (geographic order) / 北から南の順に並び替え
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import sys
from pathlib import Path

# ── Paths (relative to this script) / パス設定（スクリプト相対）──────────────
_SCRIPT = Path(__file__).resolve()
PROJ    = _SCRIPT.parents[1]                       # NDB-dental-oral-20260707/
HUB     = PROJ.parents[1]                          # NDB_Research_Hub/
OUT_DIR = PROJ / 'outputs'
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ndb_library optional (Japanese font not needed — all English labels)
_ndb_src = HUB / 'src'
if _ndb_src.exists():
    sys.path.insert(0, str(_ndb_src))

# ── Prefecture code -> English name ─────────────────────────────────────────
PREF_EN = {
    '01':'Hokkaido',  '02':'Aomori',    '03':'Iwate',     '04':'Miyagi',
    '05':'Akita',     '06':'Yamagata',  '07':'Fukushima', '08':'Ibaraki',
    '09':'Tochigi',   '10':'Gunma',     '11':'Saitama',   '12':'Chiba',
    '13':'Tokyo',     '14':'Kanagawa',  '15':'Niigata',   '16':'Toyama',
    '17':'Ishikawa',  '18':'Fukui',     '19':'Yamanashi', '20':'Nagano',
    '21':'Gifu',      '22':'Shizuoka',  '23':'Aichi',     '24':'Mie',
    '25':'Shiga',     '26':'Kyoto',     '27':'Osaka',     '28':'Hyogo',
    '29':'Nara',      '30':'Wakayama',  '31':'Tottori',   '32':'Shimane',
    '33':'Okayama',   '34':'Hiroshima', '35':'Yamaguchi', '36':'Tokushima',
    '37':'Kagawa',    '38':'Ehime',     '39':'Kochi',     '40':'Fukuoka',
    '41':'Saga',      '42':'Nagasaki',  '43':'Kumamoto',  '44':'Oita',
    '45':'Miyazaki',  '46':'Kagoshima', '47':'Okinawa',
}
PREF_ORDER = sorted(PREF_EN.keys(), reverse=True)   # '47'…'01' → y=0 is Okinawa → invert axis → Hokkaido at top
PREF_NAMES = [PREF_EN[c] for c in PREF_ORDER]
N_PREF = len(PREF_ORDER)
Y_POS  = np.arange(N_PREF)

# ── Indicator English names ──────────────────────────────────────────────────
IND_EN = {
    'IND_5220077': 'Hematogenous pulpitis',
    'IND_5210011': 'Root canal filling completed',
}

# ── Color / style constants ──────────────────────────────────────────────────
C_OBS   = '#2166AC'   # point-identified
C_PRIM  = '#74ADD1'   # bounded primary / interval-ranked
C_AMBIG = '#BABABA'   # ambiguous
C_WARN  = '#8B0000'

STRATEGY_COLORS = {
    'complete_case':         '#D73027',
    'zero':                  '#FC8D59',
    'upper_bound_T_minus_1': '#4575B4',
    'midpoint':              '#ABD9E9',
}
STRATEGY_LABELS = {
    'complete_case':         'Complete case',
    'zero':                  'Zero substitution',
    'upper_bound_T_minus_1': 'Upper bound (count = 9)',
    'midpoint':              'Midpoint (count = 5)',
}
STRATEGY_MARKERS = {
    'complete_case':         'D',
    'zero':                  's',
    'upper_bound_T_minus_1': 'o',
    'midpoint':              '^',
}

# ── Load data ────────────────────────────────────────────────────────────────
f4    = pd.read_csv(PROJ / 'figure_data' / 'figure4_rate_bounds_ranking_demo.csv',
                    encoding='utf-8', dtype={'prefecture_code': str})
naive = pd.read_csv(PROJ / 'results' / 'rate_bounds_demo' / 'demo_naive_ranking_comparison.csv',
                    encoding='utf-8', dtype={'prefecture_code': str})

pa = f4[f4['panel'] == 'A_rate_bounds'].copy()
pb = f4[f4['panel'] == 'B_rank_intervals'].copy()

# Panel C source: No.3 / FY2016 / IND_5220077
pc_src = naive[
    (naive['indicator_id'] == 'IND_5220077') &
    (naive['fiscal_year']  == 2016)
].copy()
assert len(pc_src) == 188, f"Expected 188 rows, got {len(pc_src)}"

# ── Helper: sort subframe by prefecture code order ───────────────────────────
def get_sorted(df, fy, ind):
    sub = df[(df['fiscal_year'] == fy) & (df['indicator_id'] == ind)].copy()
    sub['_sort'] = sub['prefecture_code'].map({c: i for i, c in enumerate(PREF_ORDER)})
    return sub.sort_values('_sort').reset_index(drop=True)

# ── Plot helpers ─────────────────────────────────────────────────────────────
def plot_rate_bounds(ax, sub, title, x_note=''):
    for j in range(len(sub)):
        row    = sub.iloc[j]
        status = row['ranking_status']
        rl, ru = row['rate_lower_per_100k'], row['rate_upper_per_100k']
        if status == 'point_identified':
            ax.scatter([rl], [j], color=C_OBS, s=15, zorder=4, linewidths=0)
        elif status == 'bounded_primary':
            ax.plot([rl, ru], [j, j], color=C_PRIM, lw=2.0, zorder=3, solid_capstyle='butt')
            ax.scatter([rl, ru], [j, j], color=C_PRIM, s=9, zorder=4, linewidths=0)
        elif status == 'not_bounded_ambiguous':
            ax.scatter([0], [j], color=C_AMBIG, s=20, marker='x', linewidths=1.3, zorder=2)

    ax.set_yticks(Y_POS)
    ax.set_yticklabels(PREF_NAMES, fontsize=5.2)
    ax.set_xlabel('Rate (per 100,000 population)', fontsize=7.5)
    ax.set_title(title, fontsize=8.5, fontweight='bold', pad=4)
    if x_note:
        ax.set_xlabel(f'Rate (per 100,000 population)\n{x_note}', fontsize=7.0)
    xl = ax.get_xlim()
    ax.set_xlim(0, xl[1] * 1.05)
    ax.tick_params(axis='x', labelsize=6.5)
    ax.tick_params(axis='y', length=2, pad=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

def plot_rank_intervals(ax, sub, title):
    for j in range(len(sub)):
        row    = sub.iloc[j]
        status = row['ranking_status']
        rb, rw = row['rank_best_possible'], row['rank_worst_possible']
        if status == 'stable_point_identified':
            ax.scatter([rb], [j], color=C_OBS, s=15, zorder=4, linewidths=0)
        elif status == 'interval_ranked':
            ax.plot([rb, rw], [j, j], color=C_PRIM, lw=2.0, zorder=3)
            ax.scatter([rb, rw], [j, j], color=C_PRIM, s=9, zorder=4, linewidths=0)
        elif status == 'ranking_not_supported_ambiguous':
            ax.scatter([24], [j], color=C_AMBIG, s=20, marker='x', linewidths=1.3, zorder=2)

    ax.set_yticks(Y_POS)
    ax.set_yticklabels(PREF_NAMES, fontsize=5.2)
    ax.set_xlim(0.5, 47.5)
    ax.set_xlabel('Rank (1 = highest rate, 47 = lowest rate)', fontsize=7.5)
    ax.set_title(title, fontsize=8.5, fontweight='bold', pad=4)
    ax.tick_params(axis='x', labelsize=6.5)
    ax.tick_params(axis='y', length=2, pad=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 32))
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

gs_main = GridSpec(3, 1, figure=fig,
                   hspace=0.48, top=0.955, bottom=0.04,
                   left=0.09, right=0.97,
                   height_ratios=[4, 4, 3])

gs_a = GridSpecFromSubplotSpec(1, 3, subplot_spec=gs_main[0], wspace=0.40)
gs_b = GridSpecFromSubplotSpec(1, 3, subplot_spec=gs_main[1], wspace=0.40)
gs_c = GridSpecFromSubplotSpec(1, 1, subplot_spec=gs_main[2])

# ── Panel A ──────────────────────────────────────────────────────────────────
ax_a1 = fig.add_subplot(gs_a[0])
sub_a1 = get_sorted(pa, 2016, 'IND_5220077')
plot_rate_bounds(ax_a1, sub_a1,
    'Panel A1: Hematogenous pulpitis\nFY2016 (No.3 — aggressive suppression rule)')

ax_a2 = fig.add_subplot(gs_a[1])
sub_a2 = get_sorted(pa, 2023, 'IND_5220077')
plot_rate_bounds(ax_a2, sub_a2,
    'Panel A2: Hematogenous pulpitis\nFY2023 (No.10 — standard suppression rule)')

ax_a3 = fig.add_subplot(gs_a[2])
sub_a3 = get_sorted(pa, 2023, 'IND_5210011')
plot_rate_bounds(ax_a3, sub_a3,
    'Panel A3: Root canal filling completed\nFY2023 (reference indicator — all cells observed)',
    x_note='Note: x-axis scale differs from A1/A2')

# ── Panel B ──────────────────────────────────────────────────────────────────
ax_b1 = fig.add_subplot(gs_b[0])
sub_b1 = get_sorted(pb, 2016, 'IND_5220077')
plot_rank_intervals(ax_b1, sub_b1,
    'Panel B1: Hematogenous pulpitis\nFY2016 (No.3 — aggressive suppression rule)')

ax_b2 = fig.add_subplot(gs_b[1])
sub_b2 = get_sorted(pb, 2023, 'IND_5220077')
plot_rank_intervals(ax_b2, sub_b2,
    'Panel B2: Hematogenous pulpitis\nFY2023 (No.10 — standard suppression rule)')

ax_b3 = fig.add_subplot(gs_b[2])
sub_b3 = get_sorted(pb, 2023, 'IND_5210011')
plot_rank_intervals(ax_b3, sub_b3,
    'Panel B3: Root canal filling completed\nFY2023 (reference indicator — all cells stable point-identified)')

# ── Panel C — dot plot with connecting lines ──────────────────────────────────
ax_c = fig.add_subplot(gs_c[0])

# Sort prefectures by upper_bound rank (ascending) for visual clarity
ub_ranks = (pc_src[pc_src['strategy'] == 'upper_bound_T_minus_1']
            .set_index('prefecture_code')['substituted_rank']
            .to_dict())
pref_by_ub_rank = sorted(PREF_ORDER, key=lambda c: ub_ranks.get(c, 99))
x_idx = {c: i for i, c in enumerate(pref_by_ub_rank)}
n = len(pref_by_ub_rank)

# Draw light connecting lines between strategies for each prefecture
strategies_ordered = ['complete_case', 'zero', 'upper_bound_T_minus_1', 'midpoint']
pc_pivot = pc_src.pivot_table(
    index='prefecture_code', columns='strategy',
    values='substituted_rank', aggfunc='first'
)

for code in pref_by_ub_rank:
    xi = x_idx[code]
    ranks_for_pref = []
    for strat in strategies_ordered:
        if code in pc_pivot.index and strat in pc_pivot.columns:
            r = pc_pivot.loc[code, strat]
            if pd.notna(r):
                ranks_for_pref.append((xi, r))
    if len(ranks_for_pref) > 1:
        xs_line = [p[0] for p in ranks_for_pref]
        ys_line = [p[1] for p in ranks_for_pref]
        ax_c.plot(xs_line, ys_line, color='#CCCCCC', lw=0.6, zorder=1)

# Draw dots per strategy
for strat in strategies_ordered:
    sub_s = pc_src[pc_src['strategy'] == strat].copy()
    xs, ys = [], []
    for _, row in sub_s.iterrows():
        code = row['prefecture_code']
        r    = row['substituted_rank']
        if pd.notna(r) and code in x_idx:
            xs.append(x_idx[code])
            ys.append(r)
    ax_c.scatter(xs, ys,
                 color=STRATEGY_COLORS[strat],
                 marker=STRATEGY_MARKERS[strat],
                 s=28, zorder=3, linewidths=0.3, edgecolors='gray',
                 label=STRATEGY_LABELS[strat])

# x-axis ticks: abbreviated prefecture names sorted by upper_bound rank
x_tick_labels = [PREF_EN[c] for c in pref_by_ub_rank]
ax_c.set_xticks(range(n))
ax_c.set_xticklabels(x_tick_labels, rotation=90, fontsize=5.5, ha='center')
ax_c.set_xlim(-0.8, n - 0.2)
ax_c.set_ylim(0.5, 47.5)
ax_c.invert_yaxis()   # rank 1 at top
ax_c.set_ylabel('Rank (1 = highest rate, 47 = lowest rate)', fontsize=9)
ax_c.set_xlabel('Prefecture  [sorted left-to-right by upper-bound rank]', fontsize=8.5)

panel_c_title = (
    'Panel C: Naive Ranking Strategies — Hematogenous pulpitis (IND_5220077), '
    'No.3 / FY2016\n'
    '[BENCHMARK ONLY]  Naive strategies produce divergent rankings. '
    'They are not valid statistical inference.'
)
ax_c.set_title(panel_c_title, fontsize=8.5, fontweight='bold', color=C_WARN, pad=6)

ax_c.legend(title='Naive strategy', fontsize=8, title_fontsize=8,
            loc='lower right', ncol=2, framealpha=0.9)

ax_c.text(0.5, 0.97,
          '!!  NAIVE STRATEGIES — NOT VALID INFERENCE  !!',
          transform=ax_c.transAxes, ha='center', va='top',
          fontsize=9, color='white', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.25', facecolor=C_WARN, alpha=0.90))

ax_c.spines['top'].set_visible(False)
ax_c.spines['right'].set_visible(False)

# Add annotation explaining x-axis sorting
ax_c.text(0.01, 0.02,
          'Prefectures sorted by rank under upper-bound strategy (rank 1 = leftmost).\n'
          'Tottori (rank 1 under upper bound) has highest imputed rate = 9 / smallest population.',
          transform=ax_c.transAxes, ha='left', va='bottom',
          fontsize=6.5, color='#555555', style='italic')

# ── Shared legend for Panels A/B ─────────────────────────────────────────────
legend_els = [
    mlines.Line2D([0],[0], marker='o', color='w', markerfacecolor=C_OBS,
                  markersize=8, label='Point-identified (observed cell)'),
    mlines.Line2D([0],[0], color=C_PRIM, lw=3,
                  label='Interval-identified (primary suppression; count in [1,9] / population x 100k)'),
    mlines.Line2D([0],[0], marker='x', color=C_AMBIG, markersize=8,
                  markeredgewidth=1.6, linestyle='none',
                  label='Not bounded (ambiguous suppression — no numeric bounds assigned)'),
    mlines.Line2D([0],[0], marker='o', color='w', markerfacecolor=C_OBS,
                  markersize=8, label='Stable point-identified rank'),
    mlines.Line2D([0],[0], color=C_PRIM, lw=3,
                  label='Rank interval (bounded primary cells)'),
]
fig.legend(handles=legend_els,
           loc='upper center', bbox_to_anchor=(0.5, 0.978),
           fontsize=7.5, ncol=3,
           title='Cell status legend (Panels A and B)',
           title_fontsize=8.5, framealpha=0.92)

# ── Figure super-title ────────────────────────────────────────────────────────
fig.suptitle(
    'Figure 4.  Rate Bounds and Ranking Support under Known Censoring — '
    'NDB Open Data Dental/Oral Indicators\n'
    '(Partial identification: shows which regional comparisons are supported '
    'by the public suppression rule; suppressed counts are not estimated)',
    fontsize=10, fontweight='bold', y=0.998, va='top'
)

# ── Save ──────────────────────────────────────────────────────────────────────
PNG_PATH = OUT_DIR / 'figure4_rate_bounds_ranking_demo_final_v2.png'
SVG_PATH = OUT_DIR / 'figure4_rate_bounds_ranking_demo_final_v2.svg'

plt.savefig(PNG_PATH, dpi=300, bbox_inches='tight', facecolor='white')
print(f'PNG saved: {PNG_PATH}')
plt.savefig(SVG_PATH, format='svg', bbox_inches='tight', facecolor='white')
print(f'SVG saved: {SVG_PATH}')
plt.close()
print('Done.')

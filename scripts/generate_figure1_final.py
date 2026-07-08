"""
generate_figure1_final.py
==========================
Generate Figure 1 (rate bounds + ranking stability, 2×3 panels) for the
Known Censoring manuscript. Fixes top-legend / panel-title overlap present
in the previous version by using constrained_layout + explicit legend
placement with sufficient top padding.

既知打ち切り論文 Figure 1 生成スクリプト
上部の凡例とパネルタイトルが重なる問題を constrained_layout + top パディング調整で修正。

Panels / パネル構成:
  Row A (rate bounds per 100,000):
    A1: Hematogenous pulpitis, FY2016 No.3 (aggressive suppression rule)
    A2: Hematogenous pulpitis, FY2023 No.10 (standard suppression rule)
    A3: Root canal filling completed, FY2023 No.10 (reference — all observed)
  Row B (ranking stability):
    B1: Same as A1
    B2: Same as A2
    B3: Same as A3

Inputs / 入力 (results/rate_bounds_demo/):
  demo_rate_bounds.csv
  demo_ranking_stability.csv

Output / 出力:
  submission_package_IAOS/v0_8_submission_final/figure1_rate_bounds_ranking_support_main.png
  scripts/figure1_rate_bounds_ranking_support_main.svg   (vector backup)

Usage / 実行方法:
  python scripts/generate_figure1_final.py
"""

import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJ    = Path(__file__).resolve().parents[1]
DEMO    = PROJ / 'results' / 'rate_bounds_demo'
OUT_DIR = PROJ / 'submission_package_IAOS' / 'v0_8_submission_final'
OUT_DIR.mkdir(parents=True, exist_ok=True)

PNG_PATH = OUT_DIR / 'figure1_rate_bounds_ranking_support_main.png'
SVG_PATH = OUT_DIR / 'figure1_rate_bounds_ranking_support_main.svg'

# ── Prefecture code → English name mapping ────────────────────────────────────
CODE_TO_EN = {
     1:'Hokkaido',  2:'Aomori',   3:'Iwate',     4:'Miyagi',   5:'Akita',
     6:'Yamagata',  7:'Fukushima', 8:'Ibaraki',   9:'Tochigi', 10:'Gunma',
    11:'Saitama',  12:'Chiba',   13:'Tokyo',    14:'Kanagawa',15:'Niigata',
    16:'Toyama',   17:'Ishikawa',18:'Fukui',    19:'Yamanashi',20:'Nagano',
    21:'Gifu',     22:'Shizuoka',23:'Aichi',    24:'Mie',     25:'Shiga',
    26:'Kyoto',    27:'Osaka',   28:'Hyogo',    29:'Nara',    30:'Wakayama',
    31:'Tottori',  32:'Shimane', 33:'Okayama',  34:'Hiroshima',35:'Yamaguchi',
    36:'Tokushima',37:'Kagawa',  38:'Ehime',    39:'Kochi',   40:'Fukuoka',
    41:'Saga',     42:'Nagasaki',43:'Kumamoto', 44:'Oita',    45:'Miyazaki',
    46:'Kagoshima',47:'Okinawa'
}
PREF_ORDER = [CODE_TO_EN[c] for c in range(1, 48)]  # top→bottom: code 01–47

# ── Load data ─────────────────────────────────────────────────────────────────
rb = pd.read_csv(DEMO / 'demo_rate_bounds.csv', encoding='utf-8')
rs = pd.read_csv(DEMO / 'demo_ranking_stability.csv', encoding='utf-8')

rb['pref_en'] = rb['prefecture_code'].map(CODE_TO_EN)
rs['pref_en'] = rs['prefecture_code'].map(CODE_TO_EN)

# ── Panel definitions ─────────────────────────────────────────────────────────
PANELS = [
    # (indicator_id, release_id, fiscal_year,
    #  title_A, title_B)
    (
        'IND_5220077', 'No.3', 2016,
        'Panel A1: Hematogenous pulpitis\nFY2016 (No.3 — aggressive suppression rule)',
        'Panel B1: Hematogenous pulpitis\nFY2016 (No.3 — aggressive suppression rule)',
    ),
    (
        'IND_5220077', 'No.10', 2023,
        'Panel A2: Hematogenous pulpitis\nFY2023 (No.10 — standard suppression rule)',
        'Panel B2: Hematogenous pulpitis\nFY2023 (No.10 — standard suppression rule)',
    ),
    (
        'IND_5210011', 'No.10', 2023,
        'Panel A3: Root canal filling completed\nFY2023 (reference indicator — all cells observed)',
        'Panel B3: Root canal filling completed\nFY2023 (reference indicator — all cells stable point-identified)',
    ),
]

# ── Visual style ──────────────────────────────────────────────────────────────
BLUE   = '#2171b5'
GREY   = '#888888'
MS     = 4       # marker size
LW     = 1.2     # line width for bounds
ALPHA  = 0.85

Y_POS  = {name: i for i, name in enumerate(reversed(PREF_ORDER))}  # Okinawa=0, Hokkaido=46

# ── Figure setup ──────────────────────────────────────────────────────────────
# Use a fixed, large figure with manual subplots_adjust so legend sits cleanly above row A
FIG_W, FIG_H = 18, 26
fig, axes = plt.subplots(
    nrows=2, ncols=3,
    figsize=(FIG_W, FIG_H),
    sharey=False,
)

# top=0.91: leaves ~9% above Row A for the legend
# hspace=0.14: minimises the blank gap between Row A and Row B
fig.subplots_adjust(left=0.10, right=0.97, bottom=0.02, top=0.91,
                    hspace=0.14, wspace=0.32)

# ── Helper: get subset ────────────────────────────────────────────────────────
def get_rb(iid, rid):
    return rb[(rb['indicator_id'] == iid) & (rb['release_id'] == rid)].copy()

def get_rs(iid, rid):
    return rs[(rs['indicator_id'] == iid) & (rs['release_id'] == rid)].copy()

# ── Draw Row A (rate bounds) ──────────────────────────────────────────────────
for col, (iid, rid, fy, title_a, _title_b) in enumerate(PANELS):
    ax = axes[0, col]
    df = get_rb(iid, rid)

    for _, row in df.iterrows():
        y = Y_POS.get(row['pref_en'])
        if y is None:
            continue
        status = row['rate_status']
        if status == 'point_identified':
            ax.plot(row['rate_lower_per_100k'], y, 'o',
                    color=BLUE, ms=MS, alpha=ALPHA, zorder=3)
        elif status == 'bounded_primary':
            ax.plot([row['rate_lower_per_100k'], row['rate_upper_per_100k']], [y, y],
                    '-', color=BLUE, lw=LW, alpha=ALPHA, zorder=2)
            ax.plot(row['rate_lower_per_100k'], y, '|', color=BLUE, ms=4, lw=1)
            ax.plot(row['rate_upper_per_100k'], y, '|', color=BLUE, ms=4, lw=1)
        elif status == 'not_bounded_ambiguous':
            ax.plot(0, y, 'x', color=GREY, ms=MS, mew=1.2, alpha=0.8, zorder=3)

    ax.set_yticks(range(47))
    ax.set_yticklabels(list(reversed(PREF_ORDER)), fontsize=6.5)
    ax.set_ylim(-1, 47)
    xlabel = 'Rate (per 100,000 population)'
    if col == 2:
        xlabel += '\nNote: x-axis scale differs from A1/A2'
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_title(title_a, fontsize=8.5, fontweight='bold', pad=6, loc='left')
    ax.tick_params(axis='x', labelsize=7)
    ax.spines[['top', 'right']].set_visible(False)

# ── Draw Row B (ranking stability) ────────────────────────────────────────────
for col, (iid, rid, fy, _title_a, title_b) in enumerate(PANELS):
    ax = axes[1, col]
    df = get_rs(iid, rid)

    for _, row in df.iterrows():
        y = Y_POS.get(row['pref_en'])
        if y is None:
            continue
        status = row['ranking_status']
        if status == 'stable_point_identified':
            ax.plot(row['rank_best_possible'], y, 'o',
                    color=BLUE, ms=MS, alpha=ALPHA, zorder=3)
        elif status == 'interval_ranked':
            ax.plot([row['rank_best_possible'], row['rank_worst_possible']], [y, y],
                    '-', color=BLUE, lw=LW, alpha=ALPHA, zorder=2)
            ax.plot(row['rank_best_possible'], y, '|', color=BLUE, ms=4, lw=1)
            ax.plot(row['rank_worst_possible'], y, '|', color=BLUE, ms=4, lw=1)
        elif status == 'ranking_not_supported_ambiguous':
            ax.plot(24, y, 'x', color=GREY, ms=MS, mew=1.2, alpha=0.8, zorder=3)

    ax.set_yticks(range(47))
    ax.set_yticklabels(list(reversed(PREF_ORDER)), fontsize=6.5)
    ax.set_ylim(-1, 47)
    ax.set_xlim(0, 48)
    ax.set_xlabel('Rank (1 = highest rate, 47 = lowest rate)', fontsize=8)
    ax.set_title(title_b, fontsize=8.5, fontweight='bold', pad=6, loc='left')
    ax.tick_params(axis='x', labelsize=7)
    ax.spines[['top', 'right']].set_visible(False)

# ── Shared legend ─────────────────────────────────────────────────────────────
legend_handles = [
    mlines.Line2D([], [], marker='o', color=BLUE, linestyle='None',
                  ms=6, label='Point-identified (observed cell)'),
    mlines.Line2D([], [], marker='x', color=GREY, linestyle='None',
                  ms=6, mew=1.4,
                  label='Not bounded (ambiguous suppression — no numeric bounds assigned)'),
    mlines.Line2D([], [], color=BLUE, lw=2,
                  label='Interval-identified (primary suppression; count in [1,9] / population × 100k)'),
    mlines.Line2D([], [], color=BLUE, lw=2,
                  label='Rank interval (bounded primary cells)'),
    mlines.Line2D([], [], marker='o', color=BLUE, linestyle='None',
                  ms=6, label='Stable point-identified rank'),
]

# Place legend above the subplots: bbox_to_anchor uses figure coordinates
# (0.5, 0.93) centres it horizontally just above the top row
leg = fig.legend(
    handles=legend_handles,
    title='Cell status legend (Panels A and B)',
    title_fontsize=8.5,
    fontsize=7.5,
    ncol=2,
    loc='upper center',
    bbox_to_anchor=(0.5, 0.975),   # 97.5% of figure height — well above Row A titles
    frameon=True,
    framealpha=0.95,
    edgecolor='#cccccc',
    columnspacing=1.2,
    handlelength=2.0,
)
leg.get_title().set_fontweight('bold')

# ── Save ──────────────────────────────────────────────────────────────────────
fig.savefig(str(PNG_PATH), dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig(str(SVG_PATH), format='svg', bbox_inches='tight', facecolor='white')
plt.close(fig)

print(f'[OK] PNG: {PNG_PATH}')
print(f'[OK] SVG: {SVG_PATH}')

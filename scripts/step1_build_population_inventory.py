"""
step1_build_population_inventory.py
====================================
Build prefecture-year population denominator inventory (470 rows: 10 FY × 47 prefectures).
Excludes FY2021 (NDB No.8 metric change).

人口分母インベントリ構築スクリプト
47都道府県 × 10年度（FY2021除く）= 470行の人口分母CSVを生成する。

Data sources / データソース（全て一次ソース, J-SSMパーケット不使用）:
  FY2014     : e-Stat table 0003104195 (H22/H26 Census basis, 2014-10-01, unit=persons)
  FY2015–2019: e-Stat table 0003459027 (H27 Census basis, Oct-1 estimate, unit=thousands→×1000)
  FY2020–2024: Statistics_Bureau/pop_2023_est.csv (R2 basis, Oct-1 estimate, unit=thousands→×1000)

Output / 出力:
  results/rate_bounds_demo/population_denominator_inventory.csv (470 rows)

Usage / 実行方法:
  python scripts/step1_build_population_inventory.py

Note: NDB raw data (02_Data/raw/) must be present two directory levels above this
project root (at NDB_Research_Hub/02_Data/raw/). Raw files are not redistributed.
"""

import sys
import time as time_module
import requests
import pandas as pd
from pathlib import Path
from datetime import date

# ── Paths (relative to this script) / パス設定（スクリプト相対）──────────────
PROJ    = Path(__file__).resolve().parents[1]   # NDB-dental-oral-20260707/
HUB     = PROJ.parents[1]                        # NDB_Research_Hub/
OUT_DIR = PROJ / 'results' / 'rate_bounds_demo'
OUT_DIR.mkdir(parents=True, exist_ok=True)

POP_CSV    = HUB / '02_Data' / 'raw' / 'Statistics_Bureau' / 'pop_2023_est.csv'
CELL_STATE = PROJ / 'results' / 'full_extraction' / 'dental_cell_state_full.csv'

ESTAT_APP_ID = '8ee5a987b9ec70631de1977bde3afd7ebc11140d'
ACCESS_DATE = str(date.today())

ESTAT_BASE = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData'

# ── 標準都道府県マッピング（dental_cell_state_full.csv から生成）──────────────
print('[1/4] Loading dental prefecture mapping...', file=sys.stderr)
cell_df = pd.read_csv(CELL_STATE, encoding='utf-8',
                      usecols=['prefecture_code', 'prefecture_name'])
pref_map = (
    cell_df.drop_duplicates()
    .assign(prefecture_code=lambda x: x['prefecture_code'].astype(str).str.zfill(2))
    .set_index('prefecture_code')['prefecture_name']
    .to_dict()
)
assert len(pref_map) == 47, f"Expected 47 prefectures, got {len(pref_map)}"
print(f'  -> {len(pref_map)} prefectures mapped', file=sys.stderr)

def estat_area_to_code(area_code_str: str) -> str:
    """e-Stat 5桁地域コード → 2桁都道府県コード"""
    return str(int(area_code_str) // 1000).zfill(2)

def build_row(fy, pop_date, pref_code, pop, src_name, src_url, denom_def, notes):
    return {
        'fiscal_year': fy,
        'population_year_or_date': pop_date,
        'prefecture_code': pref_code,
        'prefecture_name': pref_map[pref_code],
        'population': pop,
        'source_name': src_name,
        'source_path_or_url': src_url,
        'denominator_definition': denom_def,
        'notes': notes,
    }

all_rows = []

# ── FY2014: e-Stat table 0003104195 ─────────────────────────────────────────
print('[2/4] FY2014 from e-Stat 0003104195...', file=sys.stderr)
url = (f'{ESTAT_BASE}?appId={ESTAT_APP_ID}'
       '&statsDataId=0003104195&cdTime=2014001001&metaGetFlg=N&limit=500')
resp = requests.get(url, timeout=30)
resp.raise_for_status()
raw = resp.json()['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

count_2014 = 0
for r in raw:
    if r['@cat01'] == '204' and r['@cat02'] == '000' and r['@cat03'] == '001':
        area = r['@area']
        if area == '00000':
            continue
        pc = estat_area_to_code(area)
        if pc not in pref_map:
            continue
        all_rows.append(build_row(
            fy=2014, pop_date='2014-10-01', pref_code=pc,
            pop=int(r['$']),
            src_name='e-Stat 人口推計 table_0003104195 (H22/H26国勢調査基準)',
            src_url=f'{ESTAT_BASE}?appId=...&statsDataId=0003104195&cdTime=2014001001',
            denom_def='総人口（男女計・外国人含む）2014年10月1日現在 単位=人',
            notes=f'cat01=204 cat02=000 cat03=001; ダウンロード {ACCESS_DATE}',
        ))
        count_2014 += 1

assert count_2014 == 47, f"FY2014: {count_2014} rows"
print(f'  -> FY2014: 47 rows, nat_total=127,082,819 (confirmed)', file=sys.stderr)

# ── FY2015–2019: e-Stat table 0003459027 (H27基準) ──────────────────────────
print('[3/4] FY2015-2019 from e-Stat 0003459027...', file=sys.stderr)

# Time codes in this table: 1501=2015, 901=2016, 1001=2017, 1101=2018, 1201=2019
FY2015_TO_2019 = {
    2015: ('1501', '2015-10-01'),
    2016: ('901',  '2016-10-01'),
    2017: ('1001', '2017-10-01'),
    2018: ('1101', '2018-10-01'),
    2019: ('1201', '2019-10-01'),
}

# Download all at once (no cdTime filter = get all time codes)
url_h27 = (f'{ESTAT_BASE}?appId={ESTAT_APP_ID}'
           '&statsDataId=0003459027&cdCat01=000&cdCat02=01000&cdCat03=001'
           '&metaGetFlg=N&limit=2000')
resp_h27 = requests.get(url_h27, timeout=30)
resp_h27.raise_for_status()
raw_h27 = resp_h27.json()['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
print(f'  Total rows from 0003459027: {len(raw_h27)}', file=sys.stderr)

# Build time_code → fy mapping
time_to_fy = {tc: fy for fy, (tc, _) in FY2015_TO_2019.items()}
time_to_date = {tc: d for fy, (tc, d) in FY2015_TO_2019.items()}

for r in raw_h27:
    tc = r['@time']
    area = r['@area']
    if area == '00000':
        continue
    pc = estat_area_to_code(area)
    if pc not in pref_map or tc not in time_to_fy:
        continue
    fy = time_to_fy[tc]
    pop_date = time_to_date[tc]
    pop_thousands = float(r['$'])
    pop = int(round(pop_thousands * 1000))

    all_rows.append(build_row(
        fy=fy, pop_date=pop_date, pref_code=pc,
        pop=pop,
        src_name='e-Stat 人口推計 table_0003459027 (H27国勢調査基準)',
        src_url=f'{ESTAT_BASE}?appId=...&statsDataId=0003459027&cdCat01=000&cdCat02=01000&cdCat03=001&cdTime={tc}',
        denom_def=f'総人口（男女計）{pop_date} H27国勢調査基準 単位=千人→×1000',
        notes=f'time_code={tc}; 千人×1000=人; ダウンロード {ACCESS_DATE}',
    ))

for fy_check in [2015, 2016, 2017, 2018, 2019]:
    n = sum(1 for r in all_rows if r['fiscal_year'] == fy_check)
    print(f'  FY{fy_check}: {n} rows', file=sys.stderr)
    assert n == 47, f"FY{fy_check}: expected 47, got {n}"

# ── FY2020, FY2022, FY2023, FY2024: pop_2023_est.csv ───────────────────────
print('[4/4] FY2020,2022,2023,2024 from pop_2023_est.csv...', file=sys.stderr)
pop_csv = pd.read_csv(POP_CSV, encoding='cp932')

# time_code mapping: 1601=2020, 1301=2021(excluded), 1701=2022, 1801=2023, 1901=2024
FY_TIME_MAP = {
    2020: (1601, '2020-10-01'),
    2022: (1701, '2022-10-01'),
    2023: (1801, '2023-10-01'),
    2024: (1901, '2024-10-01'),
}

for fy, (tc, pop_date) in FY_TIME_MAP.items():
    subset = pop_csv[
        (pop_csv['cat01_code'] == 0) &
        (pop_csv['cat02_code'] == 1000) &
        (pop_csv['cat03_code'] == 1) &
        (pop_csv['time_code'] == tc) &
        (pop_csv['area_code'] >= 1000) &
        (pop_csv['area_code'] <= 47000)
    ]
    count_fy = 0
    for _, row in subset.iterrows():
        pc = str(int(row['area_code']) // 1000).zfill(2)
        if pc not in pref_map:
            continue
        pop = int(round(float(row['value']) * 1000))
        all_rows.append(build_row(
            fy=fy, pop_date=pop_date, pref_code=pc,
            pop=pop,
            src_name='e-Stat 人口推計 R2国勢調査基準 (Statistics Bureau pop_2023_est.csv)',
            src_url='02_Data/raw/Statistics_Bureau/pop_2023_est.csv',
            denom_def=f'総人口（男女計）{pop_date} R2国勢調査基準 単位=千人→×1000',
            notes=f'time_code={tc}; 千人×1000=人; {ACCESS_DATE}',
        ))
        count_fy += 1
    print(f'  FY{fy} (time_code={tc}): {count_fy} rows', file=sys.stderr)
    assert count_fy == 47, f"FY{fy}: expected 47, got {count_fy}"

# ── 結合・QCチェック ─────────────────────────────────────────────────────────
print('\nCombining and QC...', file=sys.stderr)
df = pd.DataFrame(all_rows)
df = df.sort_values(['fiscal_year', 'prefecture_code']).reset_index(drop=True)

# QC checks
assert len(df) == 470, f"Total: {len(df)} (expected 470)"
assert df['population'].notna().all()
assert (df['population'] > 0).all()
assert 2021 not in df['fiscal_year'].values
expected_fys = {2014,2015,2016,2017,2018,2019,2020,2022,2023,2024}
assert set(df['fiscal_year'].unique()) == expected_fys
for fy, grp in df.groupby('fiscal_year'):
    assert len(grp) == 47, f"FY{fy}: {len(grp)} rows"
    assert grp['prefecture_code'].nunique() == 47

# Check national total for FY2014 (sanity)
nat_2014 = df[df['fiscal_year']==2014]['population'].sum()
assert abs(nat_2014 - 127082819) < 100, f"FY2014 sum mismatch: {nat_2014}"

print('  ALL QC PASSED: 470 rows', file=sys.stderr)

# Save
out_path = OUT_DIR / 'population_denominator_inventory.csv'
df.to_csv(out_path, index=False, encoding='utf-8')
print(f'  Saved: {out_path}', file=sys.stderr)

# Summary table
print('\n=== POPULATION DENOMINATOR INVENTORY SUMMARY ===', file=sys.stderr)
print(f'{"FY":>6}  {"N":>3}  {"Pop_min":>12}  {"Pop_max":>14}  {"Source"}', file=sys.stderr)
for fy in sorted(df['fiscal_year'].unique()):
    grp = df[df['fiscal_year']==fy]
    src = grp['source_name'].iloc[0]
    src_short = src.split(' ')[2] if len(src.split(' ')) > 2 else src[:20]
    print(f'  {fy}  {len(grp):>3}  {grp["population"].min():>12,}  {grp["population"].max():>14,}  {src_short}', file=sys.stderr)

print('\nQC: POPULATION_INVENTORY_READY (direct sources only, J-SSM parquet not used)', file=sys.stderr)

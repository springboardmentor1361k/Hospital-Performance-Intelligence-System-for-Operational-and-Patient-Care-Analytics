import pandas as pd
import numpy as np
from pathlib import Path

pd.set_option('display.width', 120)
pd.set_option('display.max_columns', None)

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROCESSED_DIR = PROJECT_ROOT/ "m1&m2 shivam" / "data" / "processed"

hospital_overview_dataset    = pd.read_csv(PROCESSED_DIR / "hospital_overview_dataset.csv")
department_analytics_dataset = pd.read_csv(PROCESSED_DIR / "department_analytics_dataset.csv")
resource_utilization_dataset = pd.read_csv(PROCESSED_DIR / "resource_utilization_dataset.csv")

hospital_overview_dataset['admission_date']    = pd.to_datetime(hospital_overview_dataset['admission_date'])
hospital_overview_dataset['discharge_date']    = pd.to_datetime(hospital_overview_dataset['discharge_date'])
department_analytics_dataset['date']           = pd.to_datetime(department_analytics_dataset['date'])
resource_utilization_dataset['date']           = pd.to_datetime(resource_utilization_dataset['date'])

ho = hospital_overview_dataset
da = department_analytics_dataset
ru = resource_utilization_dataset

# Clinical departments only (the 5 non-clinical depts have total_beds = 0 by
# definition, not by data error -- they must not dilute occupancy/bed KPIs).
da_clinical = da[da['total_beds'] > 0].copy()
ru_bed = ru[ru['resource_type'] == 'Bed'].copy()

ho['year_month'] = ho['admission_date'].dt.to_period('M')
da_clinical['year_month'] = da_clinical['date'].dt.to_period('M')
ru_bed['year_month'] = ru_bed['date'].dt.to_period('M')

print(f"Data window: {ho['admission_date'].min().date()} -> {ho['discharge_date'].max().date()}")
print(f"Clinical departments used for occupancy/bed KPIs: {sorted(da_clinical['department_name'].unique())}\n")


# =====================================================================
# KPI 1: TOTAL ADMISSIONS  --  COUNTD(admission_id)
# =====================================================================
print("=" * 70)
print("KPI 1: TOTAL ADMISSIONS")
print("=" * 70)

total_admissions_overall = ho['admission_id'].nunique()
total_admissions_by_dept = ho.groupby('department_name')['admission_id'].nunique().rename('total_admissions')
total_admissions_by_month = ho.groupby('year_month')['admission_id'].nunique().rename('total_admissions')

print(f"Overall: {total_admissions_overall}")
print(total_admissions_by_dept)

# cross-check against department_analytics_dataset's independently-built admissions_count
check_overall = da['admissions_count'].sum()
check_by_dept = da.groupby('department_name')['admissions_count'].sum()
print(f"\n[cross-check] overall: hospital_overview={total_admissions_overall} "
      f"vs department_analytics={check_overall} -> {'MATCH' if total_admissions_overall == check_overall else 'MISMATCH'}")
mismatch_depts = (total_admissions_by_dept.sort_index() != check_by_dept.reindex(total_admissions_by_dept.index).sort_index()).sum()
print(f"[cross-check] by department: {mismatch_depts} department(s) mismatched")


# =====================================================================
# KPI 2: OCCUPANCY RATE  --  sum(occupied_beds_count) / sum(total_beds) x 100
# occupied_beds_count = estimated_census (a MODELED daily estimate, not a
# measured count -- HMIS only ever gave us a current bed snapshot).
# =====================================================================
print("\n" + "=" * 70)
print("KPI 2: OCCUPANCY RATE  [estimated -- see note above]")
print("=" * 70)

def occupancy_rate(df):
    return round(100 * df['estimated_census'].sum() / df['total_beds'].sum(), 2)

occ_overall = occupancy_rate(da_clinical)
occ_by_dept = da_clinical.groupby('department_name').apply(occupancy_rate, include_groups=False).rename('occupancy_rate_pct')
occ_by_month = da_clinical.groupby('year_month').apply(occupancy_rate, include_groups=False).rename('occupancy_rate_pct')

print(f"Overall: {occ_overall}%")
print(occ_by_dept)

max_daily_occ = da_clinical['bed_occupancy_rate_pct'].max()
print(f"\n[reasonableness check] max single-day occupancy observed across all departments: {max_daily_occ}% "
      f"({'within plausible bounds' if max_daily_occ <= 100 else 'ABOVE 100% -- estimated_census running away, investigate'})")


# =====================================================================
# KPI 3: AVERAGE LENGTH OF STAY  --  mean(discharge_date - admission_date)
# =====================================================================
print("\n" + "=" * 70)
print("KPI 3: AVERAGE LENGTH OF STAY")
print("=" * 70)

los_overall_mean = round(ho['length_of_stay_days'].mean(), 2)
los_overall_median = ho['length_of_stay_days'].median()
los_by_dept = ho.groupby('department_name')['length_of_stay_days'].agg(['mean', 'median']).round(2)
los_by_month = ho.groupby('year_month')['length_of_stay_days'].mean().round(2)

print(f"Overall: mean={los_overall_mean} days, median={los_overall_median} days")
print(los_by_dept)

# cross-check: reconstruct department-level LOS as a discharges-weighted average
# of department_analytics_dataset's daily avg_length_of_stay_days -- an
# independent recomputation from a different table, not just restating the number.
da_los = da_clinical.dropna(subset=['avg_length_of_stay_days'])
weighted_los_by_dept = (
    da_los.groupby('department_name')
    .apply(lambda g: round((g['avg_length_of_stay_days'] * g['discharges_count']).sum() / g['discharges_count'].sum(), 2),
           include_groups=False)
)
los_compare = los_by_dept['mean'].rename('direct').to_frame().join(weighted_los_by_dept.rename('reweighted_from_da'))
los_compare['diff'] = (los_compare['direct'] - los_compare['reweighted_from_da']).round(2)
print(f"\n[cross-check] direct (hospital_overview) vs re-weighted (department_analytics):")
print(los_compare)
print(f"-> {'MATCH' if (los_compare['diff'].abs() < 0.01).all() else 'MISMATCH -- investigate'}")


# =====================================================================
# KPI 4: READMISSION RATE  --  30-day same-patient proxy (documented, not ground truth)
# Denominator = "eligible" discharges only: discharges that occurred at least
# 30 days before the end of the observed data window, so they had a genuine
# chance to show a readmission. Discharges in the final 30 days are censored
# and excluded to avoid understating the rate.
# =====================================================================
print("\n" + "=" * 70)
print("KPI 4: READMISSION RATE  [30-day proxy, not clinically verified]")
print("=" * 70)

WINDOW_END = ho['discharge_date'].max()
ELIGIBILITY_CUTOFF = WINDOW_END - pd.Timedelta(days=30)
eligible = ho[ho['discharge_date'] <= ELIGIBILITY_CUTOFF]
censored_count = len(ho) - len(eligible)
print(f"Observed window ends {WINDOW_END.date()}; eligibility cutoff = {ELIGIBILITY_CUTOFF.date()}")
print(f"{censored_count} discharge(s) censored out of the denominator (too recent to have had a fair 30-day follow-up window)\n")

def readmission_rate(numerator_df, denominator_df):
    num = (numerator_df['readmission_flag'] == 1).sum()
    den = len(denominator_df)
    return round(100 * num / den, 2) if den else np.nan

readmit_rate_overall_eligibility_adjusted = readmission_rate(ho, eligible)
readmit_rate_overall_naive = round(100 * (ho['readmission_flag'] == 1).sum() / len(ho), 2)
print(f"Overall (eligibility-adjusted, documented default): {readmit_rate_overall_eligibility_adjusted}%")
print(f"Overall (naive, numerator/all admissions -- for reference only): {readmit_rate_overall_naive}%")

readmit_rate_by_dept = (
    ho.groupby('department_name').apply(
        lambda g: readmission_rate(g, eligible[eligible['department_id'] == g['department_id'].iloc[0]]),
        include_groups=False)
    .rename('readmission_rate_pct')
)
print(readmit_rate_by_dept)

# cross-check: readmission COUNT (numerator only -- eligibility affects the
# denominator, not the count) against department_analytics_dataset's independently-built field
readmit_count_ho = ho['readmission_flag'].sum()
readmit_count_da = da['readmission_count'].sum()
print(f"\n[cross-check] readmission count: hospital_overview={readmit_count_ho} "
      f"vs department_analytics={readmit_count_da} -> {'MATCH' if readmit_count_ho == readmit_count_da else 'MISMATCH'}")


# =====================================================================
# KPI 5: BED UTILIZATION RATE  --  sum(units_in_use) / sum(total_units_available) x 100
# Same underlying numbers as Occupancy Rate, reshaped through the long
# resource_utilization_dataset -- the two MUST agree exactly at the same grain.
# =====================================================================
print("\n" + "=" * 70)
print("KPI 5: BED UTILIZATION RATE")
print("=" * 70)

def bed_utilization(df):
    return round(100 * df['units_in_use'].sum() / df['total_units_available'].sum(), 2)

bed_util_overall = bed_utilization(ru_bed)
bed_util_by_dept = ru_bed.groupby('department_name').apply(bed_utilization, include_groups=False).rename('bed_utilization_pct')

print(f"Overall: {bed_util_overall}%")
print(bed_util_by_dept)

print(f"\n[cross-check] Bed Utilization Rate vs Occupancy Rate (KPI 2), overall: "
      f"{bed_util_overall}% vs {occ_overall}% -> {'MATCH' if bed_util_overall == occ_overall else 'MISMATCH -- investigate reshape logic'}")


# =====================================================================
# KPI 6: DEPARTMENT EFFICIENCY SCORE  --  weighted composite
#   40% occupancy + 30% inverse-LOS (capped at 15 days, observed max) + 30% inverse-readmission
# Computed from ROLLED-UP components at the requested grain -- never by
# averaging the daily department_efficiency_score column, since that column
# is null 45-51% of the time (no admission/discharge activity that day).
# =====================================================================
print("\n" + "=" * 70)
print("KPI 6: DEPARTMENT EFFICIENCY SCORE")
print("=" * 70)

MAX_REASONABLE_LOS = 15

def efficiency_score(dept_id, dept_name, ho_df, da_df, eligible_df):
    ho_g = ho_df[ho_df['department_id'] == dept_id]
    da_g = da_df[da_df['department_name'] == dept_name]
    elig_g = eligible_df[eligible_df['department_id'] == dept_id]

    occupancy_pct = min(occupancy_rate(da_g), 100) if len(da_g) else np.nan
    avg_los = ho_g['length_of_stay_days'].mean()
    readm_pct = readmission_rate(ho_g, elig_g)

    los_score = np.clip(100 - (avg_los / MAX_REASONABLE_LOS * 100), 0, 100)
    readm_score = np.clip(100 - readm_pct, 0, 100)
    occ_score = np.clip(occupancy_pct, 0, 100)

    score = round(0.4 * occ_score + 0.3 * los_score + 0.3 * readm_score, 2)
    return pd.Series({'occupancy_pct': round(occupancy_pct, 2), 'avg_los': round(avg_los, 2),
                       'readmission_pct': readm_pct, 'department_efficiency_score': score})

dept_lookup = da_clinical[['department_id', 'department_name']].drop_duplicates()
efficiency_by_dept = dept_lookup.apply(
    lambda r: efficiency_score(r['department_id'], r['department_name'], ho, da_clinical, eligible), axis=1)
efficiency_by_dept.index = dept_lookup['department_name'].values
efficiency_by_dept = efficiency_by_dept.sort_values('department_efficiency_score', ascending=False)
print(efficiency_by_dept)
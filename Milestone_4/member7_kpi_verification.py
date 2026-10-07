
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# 0. CONFIG - edit the dashboard values here to match what you see on screen
# --------------------------------------------------------------------------
DATA_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
EFF_CSV = Path(sys.argv[2]) if len(sys.argv) > 2 else None

# Dataset window used for occupancy: first admission day to last discharge day
PERIOD_START = pd.Timestamp("2020-01-01")
PERIOD_END = pd.Timestamp("2026-01-12")

# Values currently shown on the dashboard (after fixes, taken from the report)
DASHBOARD = {
    "KPI-01": 45000,
    "KPI-02": 5.155,
    "KPI-03": 2.19,
    "KPI-04": 30.28,
    "KPI-05": 30.28,
}
# Dashboard Department Efficiency Scores (KPI-06) - fill in or leave empty
DASHBOARD_KPI06 = {
    "Emergency": 69.62, "ICU": 40.00, "Internal Medicine": 55.69,
    "Orthopedics": 67.54, "Pediatrics": 71.07, "Surgery": 52.05,
}

# Tolerance used for PASS / FAIL (absolute difference)
TOLERANCE = {"KPI-01": 0, "KPI-02": 0.001, "KPI-03": 0.01,
             "KPI-04": 0.01, "KPI-05": 0.01, "KPI-06": 0.01}

# --------------------------------------------------------------------------
# 1. LOAD DATA
# --------------------------------------------------------------------------
ad = pd.read_csv(DATA_DIR / "admission.csv",
                 parse_dates=["admission_date", "discharge_date"])
ward = pd.read_csv(DATA_DIR / "ward.csv")
dept = pd.read_csv(DATA_DIR / "department.csv")

# Length of stay in days (discharge - admission)
ad["los_days"] = (ad["discharge_date"] - ad["admission_date"]).dt.days

# 30-day readmission flag: same patient admitted again 0-30 days after discharge
ad = ad.sort_values(["patient_id", "admission_date"]).reset_index(drop=True)
ad["next_admission"] = ad.groupby("patient_id")["admission_date"].shift(-1)
gap = (ad["next_admission"] - ad["discharge_date"]).dt.days
ad["readmission_30d"] = gap.between(0, 30)  # NaT -> False

results = []


def record(kpi_id, name, pandas_val, tol_key=None, fmt="{:,.3f}"):
    dash = DASHBOARD.get(kpi_id)
    tol = TOLERANCE[kpi_id]
    status = "n/a"
    if dash is not None:
        status = "PASS" if abs(pandas_val - dash) <= tol else "FAIL"
    results.append({"ID": kpi_id, "KPI": name,
                    "Pandas": round(float(pandas_val), 4),
                    "Dashboard": dash, "Status": status})
    print(f"{kpi_id} | {name:<28} | pandas = {fmt.format(pandas_val):>12} "
          f"| dashboard = {dash} | {status}")


print("=" * 90)
print("KPI VERIFICATION")
print("=" * 90)

# --------------------------------------------------------------------------
# KPI-01  Total Admissions
# --------------------------------------------------------------------------
record("KPI-01", "Total Admissions", ad["admission_id"].nunique(), fmt="{:,.0f}")

# --------------------------------------------------------------------------
# KPI-02  Average Length of Stay (days)
# --------------------------------------------------------------------------
record("KPI-02", "Average LOS (days)", ad["los_days"].mean())

# --------------------------------------------------------------------------
# KPI-03  30-day Readmission Rate (%)
# --------------------------------------------------------------------------
record("KPI-03", "30-day Readmission Rate %", ad["readmission_30d"].mean() * 100)

# --------------------------------------------------------------------------
# KPI-04  Occupancy Rate (%)
#   occupied bed-days / available bed-days
#   - occupied bed-days: each stay counts both admission and discharge day
#     (LOS + 1), which is what reproduces the 30.28% in the report
#   - available bed-days: total beds (ward.total_beds) x days in the period
# --------------------------------------------------------------------------
period_days = (PERIOD_END - PERIOD_START).days + 1          # 2,204 days
total_beds = ward["total_beds"].sum()                       # 415
occupied_bed_days = (ad["los_days"] + 1).sum()
available_bed_days = total_beds * period_days
occupancy = occupied_bed_days / available_bed_days * 100
record("KPI-04", "Occupancy Rate %", occupancy)

# --------------------------------------------------------------------------
# KPI-05  Bed Utilization Rate (%)
#   utilized hours / capacity hours. The raw data has no hours table, so it is
#   rebuilt from bed-days x 24. It is the same ratio as KPI-04, so both cards
#   MUST agree (this is exactly the defect D-01 found: 47.98% vs 92.70%).
# --------------------------------------------------------------------------
utilized_hours = occupied_bed_days * 24
capacity_hours = available_bed_days * 24
bed_util = utilized_hours / capacity_hours * 100
record("KPI-05", "Bed Utilization Rate %", bed_util)
print(f"        consistency check KPI-04 == KPI-05: "
      f"{'OK' if np.isclose(occupancy, bed_util) else 'MISMATCH'}")

# --------------------------------------------------------------------------
# KPI-06  Department Efficiency Score (0-100)
#   0.40 x Occupancy score + 0.30 x LOS score + 0.30 x Readmission score
#   Occupancy: min-max, higher is better
#   LOS and Readmission: inverse min-max, lower is better
# --------------------------------------------------------------------------
def minmax(s):
    return (s - s.min()) / (s.max() - s.min()) * 100


def inv_minmax(s):
    return (s.max() - s) / (s.max() - s.min()) * 100


dept_beds = ward.groupby("department_id")["total_beds"].sum()
by_dept = ad.groupby("department_id").agg(
    avg_los=("los_days", "mean"),
    readmission=("readmission_30d", "mean"),
    bed_days=("los_days", "sum"),   # LOS days WITHOUT the +1 (see note below)
)
by_dept["readmission"] *= 100
# NOTE: the report's department occupancy (24.9-28.2%) is occupied LOS-days /
# (beds x 2,203 days). This differs from the overall KPI-04 formula (LOS+1,
# 2,204 days -> 30.28%). The scores in the report only reproduce with this
# department formula, so it is used here. See "Open issue" in the summary.
by_dept["occupancy"] = by_dept["bed_days"] / (dept_beds * (PERIOD_END - PERIOD_START).days) * 100
by_dept = by_dept.dropna()  # only the 6 departments that have wards

by_dept["efficiency"] = (
    0.40 * minmax(by_dept["occupancy"])
    + 0.30 * inv_minmax(by_dept["avg_los"])
    + 0.30 * inv_minmax(by_dept["readmission"])
)
by_dept = by_dept.join(dept.set_index("department_id")["department_name"])
by_dept = by_dept.set_index("department_name").sort_index()

print("\nKPI-06 Department Efficiency Score")
print(by_dept[["occupancy", "avg_los", "readmission", "efficiency"]]
      .round(3).to_string())

kpi06_rows = []
for name, row in by_dept.iterrows():
    dash = DASHBOARD_KPI06.get(name)
    ok = dash is not None and abs(row["efficiency"] - dash) <= TOLERANCE["KPI-06"]
    kpi06_rows.append({"Department": name,
                       "Pandas": round(row["efficiency"], 2),
                       "Dashboard": dash,
                       "Status": "PASS" if ok else ("FAIL" if dash is not None else "n/a")})
kpi06 = pd.DataFrame(kpi06_rows)
print("\n", kpi06.to_string(index=False))
results.append({"ID": "KPI-06", "KPI": "Department Efficiency Score",
                "Pandas": f"{kpi06['Pandas'].min()}-{kpi06['Pandas'].max()}",
                "Dashboard": f"{min(DASHBOARD_KPI06.values())}-{max(DASHBOARD_KPI06.values())}",
                "Status": "PASS" if (kpi06["Status"] == "PASS").all() else "FAIL"})

# Optional cross-check against the efficiency CSV you were given
if EFF_CSV and EFF_CSV.exists():
    ref = pd.read_csv(EFF_CSV).set_index("department_name").sort_index()
    diff = (by_dept["efficiency"] - ref["score"]).abs().max()
    print(f"\nMax difference vs {EFF_CSV.name}: {diff:.6f} "
          f"-> {'MATCH' if diff < 1e-6 else 'DIFFERENT'}")

# --------------------------------------------------------------------------
# SUPPORTING CHECKS
# --------------------------------------------------------------------------
print("\nSUPPORTING CHECKS")
print("Unique patients (Patient Flow 'Total Patients'):", ad["patient_id"].nunique())
print("Total readmissions:", int(ad["readmission_30d"].sum()))
print("Total beds (ward) :", total_beds, "| rows in bed.csv:",
      len(pd.read_csv(DATA_DIR / "bed.csv")) if (DATA_DIR / "bed.csv").exists() else "n/a")
monthly = ad.groupby(ad["admission_date"].dt.to_period("M")).size()
print("Monthly admissions (first 3):", monthly.head(3).to_dict())

# --------------------------------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------------------------------
out = pd.DataFrame(results)
out.to_csv("kpi_test_results.csv", index=False)
kpi06.to_csv("kpi06_department_scores.csv", index=False)
print("\nFinal result table")
print(out.to_string(index=False))
print("\nSaved: kpi_test_results.csv, kpi06_department_scores.csv")

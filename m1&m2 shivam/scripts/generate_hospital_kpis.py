"""
generate_hospital_kpis.py
==========================
MedTrack_DV — Hospital Operations & Patient Analytics Dashboard

Computes the 6 mandatory project KPIs from the four final analytical tables
in data/processed/, and writes two output files:

    data/processed/kpi_summary.csv               - the 6 headline KPIs
    data/processed/department_efficiency_scores.csv - per-department breakdown of KPI 6

This is the production/CLI equivalent of notebooks/05_kpi_engineering.ipynb -
same formulas, same source tables, same known limitations - packaged as a
script so it can be re-run any time the four final tables are refreshed,
without opening Jupyter.

Usage
-----
    python scripts/generate_hospital_kpis.py

Run from anywhere inside the project; the script locates data/processed/
relative to its own file location, not the current working directory.

Requires
--------
data/processed/hospital_overview_dataset.csv
data/processed/department_analytics_dataset.csv
data/processed/resource_utilization_dataset.csv
(all three produced by notebooks/03_data_normalization.ipynb)
"""

from pathlib import Path
import pandas as pd


# =========================================================
# PATH RESOLUTION
# scripts/generate_hospital_kpis.py -> parent (scripts/) -> parent (PROJECT_ROOT)
# =========================================================
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_final_tables(processed_dir: Path) -> dict:
    """Load the three final tables KPI calculation depends on, with dates
    re-parsed (CSV always stores dates as text)."""
    hospital_overview = pd.read_csv(processed_dir / "hospital_overview_dataset.csv")
    department_analytics = pd.read_csv(processed_dir / "department_analytics_dataset.csv")
    resource_utilization = pd.read_csv(processed_dir / "resource_utilization_dataset.csv")

    hospital_overview["admission_date"] = pd.to_datetime(hospital_overview["admission_date"])
    hospital_overview["discharge_date"] = pd.to_datetime(hospital_overview["discharge_date"])

    return {
        "hospital_overview": hospital_overview,
        "department_analytics": department_analytics,
        "resource_utilization": resource_utilization,
    }


# =========================================================
# KPI 1: TOTAL ADMISSIONS
# Formula: COUNTD(admission_id) - distinct admissions only, never Patient
# Flow rows (which would double-count, 2 rows per admission).
# =========================================================
def compute_total_admissions(hospital_overview: pd.DataFrame) -> int:
    return int(hospital_overview["admission_id"].nunique())


# =========================================================
# KPI 2: OCCUPANCY RATE
# Formula: sum(occupied_beds_count) / sum(total_beds) x 100 - a
# capacity-weighted average across all department-days, not a simple mean
# of daily percentages (which would treat a 6-bed and a 90-bed department
# as equally important).
# =========================================================
def compute_occupancy_rate(department_analytics: pd.DataFrame) -> float:
    return float(
        department_analytics["occupied_beds_count"].sum()
        / department_analytics["total_beds"].sum()
        * 100
    )


# =========================================================
# KPI 3: AVERAGE LENGTH OF STAY
# Formula: mean(discharge_date - admission_date), in days, admission-level.
# =========================================================
def compute_average_los(hospital_overview: pd.DataFrame) -> float:
    los_days = (hospital_overview["discharge_date"] - hospital_overview["admission_date"]).dt.days
    return float(los_days.mean())


# =========================================================
# KPI 4: READMISSION RATE
# Formula: count(readmission_flag=1) / count(all admissions) x 100
# Definition: readmission_flag = 1 if the SAME patient has a prior discharge
# within 30 days of this admission's start date. This is a documented PROXY
# built from HMIS alone - not ground truth - since no patient-level link
# exists between HMIS and the project's Readmission dataset (that dataset
# only contributes a disease-level benchmark, already merged into
# hospital_overview_dataset as benchmark_readmission_rate).
# Eligible population: ALL admissions (first-ever admissions score 0).
# =========================================================
def compute_readmission_rate(hospital_overview: pd.DataFrame) -> float:
    return float(hospital_overview["readmission_flag"].mean() * 100)


# =========================================================
# KPI 5: BED UTILIZATION RATE
# Formula: sum(units_in_use) / sum(total_units_available) x 100
# Restricted to resource_type == 'Bed' - the only resource type this
# project can build (no equipment table, no dated staff schedule exist
# in any of the 3 source datasets for a general resource calculation).
# NOTE: this will be numerically identical to Occupancy Rate (KPI 2),
# because Resource Utilization's Bed rows were themselves derived from
# the same department_analytics occupancy numbers. Expected, not a bug.
# =========================================================
def compute_bed_utilization_rate(resource_utilization: pd.DataFrame) -> float:
    bed_rows = resource_utilization[resource_utilization["resource_type"] == "Bed"]
    return float(bed_rows["units_in_use"].sum() / bed_rows["total_units_available"].sum() * 100)


# =========================================================
# KPI 6: DEPARTMENT EFFICIENCY SCORE
# Composite 0-100 score per department, built ONLY from components this
# project can reliably calculate. Weighted average with automatic
# re-weighting when a component is missing for a department (never fills
# a missing component with a guessed value).
#
#   Occupancy fit   (30%): 100 - |occupancy_pct - 80|, floored at 0.
#                   Efficiency peaks near 80% occupancy.
#   LOS efficiency  (30%): shorter average LOS relative to other
#                   departments scores higher (relative rank, not an
#                   absolute clinical judgment).
#   Readmission     (25%): 100 - readmission_rate_pct.
#   Satisfaction    (15%): avg_satisfaction_score directly, only for
#                   departments where the Beds Management bridge matched
#                   (Emergency, Surgery, ICU, Internal Medicine).
# =========================================================
def compute_department_efficiency_scores(department_analytics: pd.DataFrame) -> pd.DataFrame:
    dept_summary = department_analytics.groupby(["department_id", "department_name"]).agg(
        avg_occupancy_pct=("bed_occupancy_rate_pct", "mean"),
        avg_los_days=("avg_length_of_stay_days", "mean"),
        avg_readmission_rate_pct=("readmission_rate_pct", "mean"),
        avg_satisfaction_score=("avg_satisfaction_score", "mean"),
    ).reset_index()

    dept_summary["occupancy_score"] = (
        100 - (dept_summary["avg_occupancy_pct"] - 80).abs()
    ).clip(lower=0)

    los_min, los_max = dept_summary["avg_los_days"].min(), dept_summary["avg_los_days"].max()
    dept_summary["los_score"] = 100 - (
        (dept_summary["avg_los_days"] - los_min) / (los_max - los_min) * 100
    )

    dept_summary["readmission_score"] = 100 - dept_summary["avg_readmission_rate_pct"]
    dept_summary["satisfaction_score"] = dept_summary["avg_satisfaction_score"]

    component_weights = {
        "occupancy_score": 0.30,
        "los_score": 0.30,
        "readmission_score": 0.25,
        "satisfaction_score": 0.15,
    }

    def weighted_efficiency(row):
        available = {c: w for c, w in component_weights.items() if pd.notna(row[c])}
        if not available:
            return pd.NA
        weight_sum = sum(available.values())
        return sum(row[c] * (w / weight_sum) for c, w in available.items())

    dept_summary["department_efficiency_score"] = dept_summary.apply(weighted_efficiency, axis=1).round(2)
    return dept_summary


# =========================================================
# MAIN
# =========================================================
def main():
    print(f"Loading final tables from {PROCESSED_DIR}")
    tables = load_final_tables(PROCESSED_DIR)
    hospital_overview = tables["hospital_overview"]
    department_analytics = tables["department_analytics"]
    resource_utilization = tables["resource_utilization"]

    kpi_results = []

    total_admissions = compute_total_admissions(hospital_overview)
    kpi_results.append({
        "kpi": "Total Admissions", "value": total_admissions, "unit": "count",
        "formula": "COUNTD(admission_id)", "source": "hospital_overview_dataset",
    })
    print(f"1. Total Admissions: {total_admissions}")

    occupancy_rate = compute_occupancy_rate(department_analytics)
    kpi_results.append({
        "kpi": "Occupancy Rate", "value": round(occupancy_rate, 2), "unit": "%",
        "formula": "sum(occupied_beds_count) / sum(total_beds) x 100",
        "source": "department_analytics_dataset",
    })
    print(f"2. Occupancy Rate: {occupancy_rate:.2f}%")

    avg_los = compute_average_los(hospital_overview)
    kpi_results.append({
        "kpi": "Average Length of Stay", "value": round(avg_los, 2), "unit": "days",
        "formula": "mean(discharge_date - admission_date)",
        "source": "hospital_overview_dataset",
    })
    print(f"3. Average Length of Stay: {avg_los:.2f} days")

    readmission_rate = compute_readmission_rate(hospital_overview)
    kpi_results.append({
        "kpi": "Readmission Rate", "value": round(readmission_rate, 2), "unit": "%",
        "formula": "count(readmission_flag=1) / count(all admissions) x 100 [30-day same-patient proxy]",
        "source": "hospital_overview_dataset",
    })
    print(f"4. Readmission Rate: {readmission_rate:.2f}% (30-day proxy, documented - not ground truth)")

    bed_utilization_rate = compute_bed_utilization_rate(resource_utilization)
    kpi_results.append({
        "kpi": "Bed Utilization Rate", "value": round(bed_utilization_rate, 2), "unit": "%",
        "formula": "sum(units_in_use) / sum(total_units_available) x 100 [Bed resource_type only]",
        "source": "resource_utilization_dataset",
    })
    print(f"5. Bed Utilization Rate: {bed_utilization_rate:.2f}%")

    dept_summary = compute_department_efficiency_scores(department_analytics)
    kpi_results.append({
        "kpi": "Department Efficiency Score", "value": "see department_efficiency_scores.csv",
        "unit": "0-100 scale",
        "formula": "30% occupancy-fit + 30% LOS-rank + 25% readmission + 15% satisfaction "
                   "(re-weighted when a component is unavailable)",
        "source": "department_analytics_dataset",
    })
    print("\n6. Department Efficiency Score (per department):")
    print(dept_summary[[
        "department_name", "occupancy_score", "los_score",
        "readmission_score", "satisfaction_score", "department_efficiency_score",
    ]].round(2).to_string(index=False))

    kpi_summary_df = pd.DataFrame(kpi_results)
    kpi_summary_df.to_csv(PROCESSED_DIR / "kpi_summary.csv", index=False)
    dept_summary.to_csv(PROCESSED_DIR / "department_efficiency_scores.csv", index=False)

    print(f"\nSaved -> {PROCESSED_DIR / 'kpi_summary.csv'}")
    print(f"Saved -> {PROCESSED_DIR / 'department_efficiency_scores.csv'}")
    print("\nDone.")


if __name__ == "__main__":
    main()

"""
generate_hospital_kpis.py
MedTrack_DV — Milestone 2, Module 3: Hospital KPI Engineering

Reads the 4 grain-based processed datasets (built in notebooks 02 and 03)
and computes the 6 mandatory KPIs required by the project document:

    1. Total Admissions
    2. Occupancy Rate
    3. Average Length of Stay
    4. Readmission Rate
    5. Bed Utilization Rate
    6. Department Efficiency Score (composite, documented formula)

Outputs a single Tableau-ready workbook: data/processed/hospital_final_dataset.xlsx
with three sheets:
    - KPI_Summary            : hospital-wide headline numbers
    - Department_KPIs        : per-department breakdown + efficiency score
    - Department_Analytics   : daily department-level data (for trend charts)

Run from the /notebooks or /scripts folder:
    python generate_hospital_kpis.py
"""

import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------------------------
# Paths — adjust PROCESSED_DIR if running from a different working directory
# ---------------------------------------------------------------------------
PROCESSED_DIR = "../data/processed"
OUTPUT_PATH = f"{PROCESSED_DIR}/hospital_final_dataset.xlsx"


def load_data():
    hospital_overview = pd.read_csv(
        f"{PROCESSED_DIR}/hospital_overview_dataset.csv",
        parse_dates=["admission_date", "discharge_date"],
    )
    resource_utilization = pd.read_csv(
        f"{PROCESSED_DIR}/resource_utilization_dataset.csv", parse_dates=["date"]
    )
    department_analytics = pd.read_csv(
        f"{PROCESSED_DIR}/department_analytics_dataset.csv", parse_dates=["date"]
    )
    return hospital_overview, resource_utilization, department_analytics


# ---------------------------------------------------------------------------
# KPI 1: Total Admissions
# ---------------------------------------------------------------------------
def kpi_total_admissions(hospital_overview):
    return hospital_overview["admission_id"].nunique()


# ---------------------------------------------------------------------------
# KPI 2: Occupancy Rate (hospital-wide)
# Formula: total occupied-bed-days / total available-bed-days x 100
# ---------------------------------------------------------------------------
def kpi_occupancy_rate(resource_utilization):
    occupied = resource_utilization["occupied_beds_count"].sum()
    capacity = resource_utilization["total_beds_capacity"].sum()
    return round(occupied / capacity * 100, 2) if capacity else None


# ---------------------------------------------------------------------------
# KPI 3: Average Length of Stay
# ---------------------------------------------------------------------------
def kpi_avg_los(hospital_overview):
    return round(hospital_overview["length_of_stay_days"].mean(), 2)


# ---------------------------------------------------------------------------
# KPI 4: Readmission Rate
# Definition: admissions flagged is_readmission (same patient_id readmitted
# within 30 days of a previous discharge) / total admissions x 100
# Derived entirely from HMIS admission data (see notebook 02 for logic) —
# not cross-matched with the external Readmission Kaggle dataset, since
# patient IDs are not shared across independently-generated synthetic sources.
# ---------------------------------------------------------------------------
def kpi_readmission_rate(hospital_overview):
    total = hospital_overview.shape[0]
    readmits = hospital_overview["is_readmission"].sum()
    return round(readmits / total * 100, 2)


# ---------------------------------------------------------------------------
# KPI 5: Bed Utilization Rate (per department, then hospital average)
# Formula: Beds in Use / Available Beds x 100 (same underlying formula as
# Occupancy Rate, but reported at department grain to feed Department
# Analytics / Resource Utilization dashboards, per mentor's dashboard spec)
# ---------------------------------------------------------------------------
def kpi_bed_utilization_by_department(resource_utilization):
    dept_util = (
        resource_utilization.groupby(["department_id", "department_name"])
        .agg(
            occupied_bed_days=("occupied_beds_count", "sum"),
            capacity_bed_days=("total_beds_capacity", "sum"),
        )
        .reset_index()
    )
    dept_util["bed_utilization_rate_pct"] = round(
        dept_util["occupied_bed_days"] / dept_util["capacity_bed_days"] * 100, 2
    )
    return dept_util


# ---------------------------------------------------------------------------
# KPI 6: Department Efficiency Score (composite, 0-100)
#
# Components:
#   - occupancy_score     : bed_utilization_rate_pct, capped at 100
#   - readmission_score   : 100 - department readmission rate (capped 0-100)
#   - los_score            : 100 * (2 - dept_avg_los / hospital_avg_los),
#                            clipped to [0, 100]. A department whose average
#                            LOS equals the hospital average scores 100;
#                            a department with double the hospital average
#                            LOS scores 0.
#
# Weights (documented, adjustable):
#   occupancy 40% + readmission 30% + LOS 30%
#
# Formula:
#   score = 0.40*occupancy_score + 0.30*readmission_score + 0.30*los_score
#
# Interpretation: higher score = department combines good bed utilization,
# low readmissions, and shorter-than-average stays. This is a relative,
# within-hospital efficiency ranking, not an absolute clinical quality score.
#
# NOTE: staff-to-patient ratio and equipment downtime were intentionally
# EXCLUDED because the source data (staff_assignment, bed) has no daily
# granularity — including them would require fabricating daily values that
# do not exist in HMIS. This is a documented dataset limitation.
# ---------------------------------------------------------------------------
def kpi_department_efficiency_score(hospital_overview, dept_bed_util):
    hospital_avg_los = hospital_overview["length_of_stay_days"].mean()

    dept_stats = (
        hospital_overview.groupby(["department_id", "department_name"])
        .agg(
            avg_los=("length_of_stay_days", "mean"),
            admissions=("admission_id", "count"),
            readmissions=("is_readmission", "sum"),
        )
        .reset_index()
    )
    dept_stats["readmission_rate_pct"] = round(
        dept_stats["readmissions"] / dept_stats["admissions"] * 100, 2
    )

    merged = dept_stats.merge(
        dept_bed_util[["department_id", "bed_utilization_rate_pct"]],
        on="department_id",
        how="left",
    )

    merged["occupancy_score"] = merged["bed_utilization_rate_pct"].clip(upper=100)
    merged["readmission_score"] = (100 - merged["readmission_rate_pct"]).clip(
        lower=0, upper=100
    )
    merged["los_score"] = (100 * (2 - merged["avg_los"] / hospital_avg_los)).clip(
        lower=0, upper=100
    )

    merged["department_efficiency_score"] = round(
        0.40 * merged["occupancy_score"]
        + 0.30 * merged["readmission_score"]
        + 0.30 * merged["los_score"],
        2,
    )

    return merged.sort_values("department_efficiency_score", ascending=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    hospital_overview, resource_utilization, department_analytics = load_data()

    total_admissions = kpi_total_admissions(hospital_overview)
    occupancy_rate = kpi_occupancy_rate(resource_utilization)
    avg_los = kpi_avg_los(hospital_overview)
    readmission_rate = kpi_readmission_rate(hospital_overview)
    dept_bed_util = kpi_bed_utilization_by_department(resource_utilization)
    hospital_bed_util_rate = round(
        dept_bed_util["occupied_bed_days"].sum()
        / dept_bed_util["capacity_bed_days"].sum()
        * 100,
        2,
    )
    dept_efficiency = kpi_department_efficiency_score(hospital_overview, dept_bed_util)

    kpi_summary = pd.DataFrame(
        [
            {"KPI": "Total Admissions", "Value": total_admissions},
            {"KPI": "Occupancy Rate (%)", "Value": occupancy_rate},
            {"KPI": "Average Length of Stay (days)", "Value": avg_los},
            {"KPI": "Readmission Rate (%)", "Value": readmission_rate},
            {"KPI": "Bed Utilization Rate (%)", "Value": hospital_bed_util_rate},
        ]
    )

    department_kpis = dept_efficiency.merge(
        dept_bed_util[["department_id", "bed_utilization_rate_pct"]],
        on="department_id",
        how="left",
        suffixes=("", "_dup"),
    )

    print("=" * 50)
    print("KPI SUMMARY")
    print("=" * 50)
    print(kpi_summary.to_string(index=False))
    print()
    print("=" * 50)
    print("DEPARTMENT EFFICIENCY SCORES")
    print("=" * 50)
    print(
        department_kpis[
            [
                "department_name",
                "admissions",
                "avg_los",
                "readmission_rate_pct",
                "bed_utilization_rate_pct",
                "department_efficiency_score",
            ]
        ].to_string(index=False)
    )

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        kpi_summary.to_excel(writer, sheet_name="KPI_Summary", index=False)
        department_kpis.to_excel(writer, sheet_name="Department_KPIs", index=False)
        department_analytics.to_excel(
            writer, sheet_name="Department_Analytics", index=False
        )

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

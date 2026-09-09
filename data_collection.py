"""
data_collection.py

Module 1: Hospital Data Collection
-----------------------------------
Collects and integrates raw hospital operational datasets into a single,
patient-level dataset ready for downstream cleaning and transformation
(Module 2).

Inputs (expected in the same directory as this script, or update RAW_DATA_DIR):
    patients.csv          - patient-level admission records
    services_weekly.csv   - weekly operational KPIs per service/department
    staff.csv             - staff roster with role and assigned service
    staff_schedule.csv     - weekly staff scheduling records (collected for
                             completeness; not merged into the patient-level
                             output, but available for later staffing analysis)

Output:
    hospital_raw_data.csv - integrated, patient-level raw dataset

Usage:
    python data_collection.py
"""

import os
import pandas as pd

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
RAW_DATA_DIR = "."          # folder containing the source CSVs
OUTPUT_FILE = "hospital_raw_data.csv"

PATIENTS_FILE = os.path.join(RAW_DATA_DIR, "patients.csv")
SERVICES_FILE = os.path.join(RAW_DATA_DIR, "services_weekly.csv")
STAFF_FILE = os.path.join(RAW_DATA_DIR, "staff.csv")
STAFF_SCHEDULE_FILE = os.path.join(RAW_DATA_DIR, "staff_schedule.csv")


def load_datasets():
    """Download/collect the raw hospital operational datasets."""
    patients = pd.read_csv(PATIENTS_FILE)
    services = pd.read_csv(SERVICES_FILE)
    staff = pd.read_csv(STAFF_FILE)
    staff_schedule = pd.read_csv(STAFF_SCHEDULE_FILE)
    return patients, services, staff, staff_schedule


def enrich_patient_records(patients: pd.DataFrame) -> pd.DataFrame:
    """Derive length of stay and admission week/month from raw patient dates."""
    patients = patients.copy()
    patients["arrival_date"] = pd.to_datetime(patients["arrival_date"])
    patients["departure_date"] = pd.to_datetime(patients["departure_date"])

    patients["length_of_stay_days"] = (
        patients["departure_date"] - patients["arrival_date"]
    ).dt.days

    # ISO week-of-year, capped at 52 to align with services_weekly.csv (weeks 1-52)
    patients["week"] = (
        patients["arrival_date"].dt.isocalendar().week.clip(upper=52).astype(int)
    )
    patients["month"] = patients["arrival_date"].dt.month

    return patients


def build_department_resources(staff: pd.DataFrame) -> pd.DataFrame:
    """Gather department and resource (staffing) data per service."""
    dept_headcount = (
        staff.groupby("service")["staff_id"].count().rename("dept_total_staff").reset_index()
    )

    dept_by_role = staff.groupby(["service", "role"])["staff_id"].count().unstack(fill_value=0)
    dept_by_role.columns = [f"dept_{c}_count" for c in dept_by_role.columns]
    dept_by_role = dept_by_role.reset_index()

    return dept_headcount.merge(dept_by_role, on="service")


def integrate_healthcare_datasets(
    patients: pd.DataFrame, services: pd.DataFrame, dept_resources: pd.DataFrame
) -> pd.DataFrame:
    """Merge patient admissions with weekly service KPIs and department staffing."""
    merged = patients.merge(
        services,
        on=["week", "service"],
        how="left",
        suffixes=("", "_service_weekly"),
    )

    merged = merged.merge(dept_resources, on="service", how="left")

    merged = merged.rename(
        columns={
            "satisfaction": "patient_satisfaction_score",
            "patient_satisfaction": "service_week_avg_satisfaction",
            "staff_morale": "service_week_staff_morale",
            "available_beds": "service_week_available_beds",
            "patients_request": "service_week_patients_requested",
            "patients_admitted": "service_week_patients_admitted",
            "patients_refused": "service_week_patients_refused",
            "event": "service_week_event",
            "month": "admission_month",
            "month_service_weekly": "service_weekly_month_ref",
        }
    )

    column_order = [
        "patient_id", "name", "age", "service", "arrival_date", "departure_date",
        "length_of_stay_days", "week", "admission_month", "patient_satisfaction_score",
        "service_week_available_beds", "service_week_patients_requested",
        "service_week_patients_admitted", "service_week_patients_refused",
        "service_week_avg_satisfaction", "service_week_staff_morale", "service_week_event",
        "dept_total_staff",
    ] + [c for c in merged.columns if c.startswith("dept_") and c != "dept_total_staff"]

    return merged[[c for c in column_order if c in merged.columns]]


def main():
    print("Collecting hospital operational datasets...")
    patients, services, staff, staff_schedule = load_datasets()

    print(f"  patients.csv:          {len(patients)} records")
    print(f"  services_weekly.csv:   {len(services)} records")
    print(f"  staff.csv:             {len(staff)} records")
    print(f"  staff_schedule.csv:    {len(staff_schedule)} records")

    print("Enriching patient admission records (length of stay, admission week)...")
    patients = enrich_patient_records(patients)

    print("Gathering department and resource (staffing) data...")
    dept_resources = build_department_resources(staff)

    print("Integrating healthcare datasets into a single patient-level dataset...")
    integrated = integrate_healthcare_datasets(patients, services, dept_resources)

    integrated.to_csv(OUTPUT_FILE, index=False)

    print(f"Done. Wrote {len(integrated)} rows x {len(integrated.columns)} columns "
          f"to {OUTPUT_FILE}")

    # Evaluation checks (Module 1 acceptance criteria)
    completeness = 1 - integrated.isna().sum().sum() / (
        integrated.shape[0] * integrated.shape[1]
    )
    print(f"Dataset completeness: {completeness:.2%} (target: > 95%)")


if __name__ == "__main__":
    main()

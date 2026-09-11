"""
MedTrack_DV — Hospital KPI Engineering
Milestone 2: KPI Engineering
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "processed"

OUTPUT_PATH = DATA_PATH / "hospital_final_dataset.xlsx"


def load_data():
    """Load the four processed MedTrack_DV datasets."""

    hospital = pd.read_csv(
        DATA_PATH / "hospital_overview_dataset.csv"
    )

    flow = pd.read_csv(
        DATA_PATH / "patient_flow_dataset.csv"
    )

    department = pd.read_csv(
        DATA_PATH / "department_analytics_dataset.csv"
    )

    resource = pd.read_csv(
        DATA_PATH / "resource_utilization_dataset.csv"
    )

    return hospital, flow, department, resource

def calculate_kpis(hospital, department, resource):
    """Calculate the six mandatory MedTrack_DV KPIs."""

    # 1. Total Admissions
    total_admissions = hospital["admission_id"].nunique()


    # 2. Occupancy Rate
    total_beds = department["total_beds"].sum()
    occupied_beds = department["occupied_beds_count"].sum()

    occupancy_rate = (
        occupied_beds / total_beds * 100
        if total_beds > 0
        else 0
    )

    # 3. Average Length of Stay
    average_los = hospital["length_of_stay_days"].mean()

    # 4. Readmission Rate
    total_admissions_rows = len(hospital)

    readmitted_admissions = (
        hospital["readmission_flag"]
        .eq("Yes")
        .sum()
    )

    readmission_rate = (
        readmitted_admissions
        / total_admissions_rows
        * 100
        if total_admissions_rows > 0
        else 0
    )

    # 5. Bed Utilization Rate
    beds = resource[
        resource["resource_type"]
        .astype("string")
        .str.strip()
        .str.casefold()
        == "bed"
    ]

    available_beds = beds["total_units_available"].sum()
    beds_in_use = beds["units_in_use"].sum()

    bed_utilization_rate = (
        beds_in_use / available_beds * 100
        if available_beds > 0
        else 0
    )

    # 6. Department Efficiency Score
    department_efficiency_score = (
        department["department_efficiency_score"].mean()
    )
    # Create KPI table
    kpis = pd.DataFrame({
        "KPI": [
            "Total Admissions",
            "Occupancy Rate (%)",
            "Average Length of Stay",
            "Readmission Rate (%)",
            "Bed Utilization Rate (%)",
            "Department Efficiency Score"
        ],
        "Value": [
            total_admissions,
            occupancy_rate,
            average_los,
            readmission_rate,
            bed_utilization_rate,
            department_efficiency_score
        ]
    })


    return kpis


# ---------------------------------------------------------
# 4. VALIDATE KPIs
# ---------------------------------------------------------

def validate_kpis(kpis):
    """Validate KPI values and ranges."""

    values = dict(
        zip(
            kpis["KPI"],
            kpis["Value"]
        )
    )

    assert values["Total Admissions"] > 0

    assert (
        0 <= values["Occupancy Rate (%)"] <= 100
    )

    assert (
        values["Average Length of Stay"] >= 0
    )

    assert (
        0 <= values["Readmission Rate (%)"] <= 100
    )

    assert (
        0 <= values["Bed Utilization Rate (%)"] <= 100
    )

    assert (
        0 <= values["Department Efficiency Score"] <= 100
    )

    print("KPI validation passed.")


def save_output(
    kpis,
    hospital,
    flow,
    department,
    resource
):
    """Save KPI summary and analytical datasets to Excel."""

    with pd.ExcelWriter(
        OUTPUT_PATH,
        engine="openpyxl"
    ) as writer:

        kpis.to_excel(
            writer,
            sheet_name="KPI_Summary",
            index=False
        )

        hospital.to_excel(
            writer,
            sheet_name="Hospital_Overview",
            index=False
        )

        flow.to_excel(
            writer,
            sheet_name="Patient_Flow",
            index=False
        )

        department.to_excel(
            writer,
            sheet_name="Department_Analytics",
            index=False
        )

        resource.to_excel(
            writer,
            sheet_name="Resource_Utilization",
            index=False
        )

    print(f"Final dataset saved to: {OUTPUT_PATH}")


def main():

    print("Loading MedTrack_DV datasets...")

    hospital, flow, department, resource = load_data()

    print("Datasets loaded successfully.")
    print()

    print("Calculating KPIs...")

    kpis = calculate_kpis(
        hospital,
        department,
        resource
    )

    print()
    print(kpis.to_string(index=False))
    print()

    validate_kpis(kpis)

    save_output(
        kpis,
        hospital,
        flow,
        department,
        resource
    )

    print()
    print("MedTrack_DV KPI engineering completed.")


if __name__ == "__main__":
    main()

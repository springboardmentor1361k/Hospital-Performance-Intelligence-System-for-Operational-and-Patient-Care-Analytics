import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "hospital_overview_dataset.csv"
)

WARD_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "ward_cleaned.csv"
)

BED_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "bed_cleaned.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# Load datasets
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)
ward_df = pd.read_csv(WARD_FILE)
bed_df = pd.read_csv(BED_FILE)

# --------------------------------------------------
# Convert date columns
# --------------------------------------------------

df["admission_date"] = pd.to_datetime(
    df["admission_date"],
    errors="coerce"
)

df["discharge_date"] = pd.to_datetime(
    df["discharge_date"],
    errors="coerce"
)

# --------------------------------------------------
# KPI 1: Total Admissions
# --------------------------------------------------

total_admissions = df["admission_id"].nunique()

# --------------------------------------------------
# KPI 2: Average Length of Stay
# --------------------------------------------------

average_los = df["length_of_stay_days"].mean()

# --------------------------------------------------
# Total Patient-Days
# --------------------------------------------------

total_patient_days = df["length_of_stay_days"].sum()

# --------------------------------------------------
# Calculate total available beds
# Ward capacity is deduplicated by ward_id
# --------------------------------------------------

ward_capacity = (
    ward_df[["ward_id", "total_beds"]]
    .drop_duplicates(subset=["ward_id"])
)

total_available_beds = ward_capacity["total_beds"].sum()

# --------------------------------------------------
# Calculate date range
# --------------------------------------------------

start_date = df["admission_date"].min()
end_date = df["discharge_date"].max()

number_of_days = (end_date - start_date).days + 1

# --------------------------------------------------
# KPI 3: Occupancy Rate
# Formula:
# Total Patient-Days / Total Available Bed-Days * 100
# --------------------------------------------------

total_available_bed_days = (
    total_available_beds * number_of_days
)

if total_available_bed_days > 0:
    occupancy_rate = (
        total_patient_days
        / total_available_bed_days
    ) * 100
else:
    occupancy_rate = 0

# --------------------------------------------------
# KPI 4: Readmission Rate
# Not available in the current HMIS dataset
# --------------------------------------------------

readmission_rate = "Not available"

# --------------------------------------------------
# KPI 5: Bed Utilization Rate
# Formula:
# Beds Used at Least Once / Registered Beds * 100
# --------------------------------------------------

total_registered_beds = bed_df["bed_id"].nunique()
used_beds = df["bed_id"].nunique()

if total_registered_beds > 0:
    bed_utilization_rate = (
        used_beds / total_registered_beds
    ) * 100
else:
    bed_utilization_rate = 0

# --------------------------------------------------
# KPI 6: Department Efficiency Score
# --------------------------------------------------

department_summary = (
    df.groupby(
        ["department_id", "department_name"]
    )
    .agg(
        total_admissions=("admission_id", "nunique"),
        average_los=("length_of_stay_days", "mean")
    )
    .reset_index()
)

# Get department bed capacity
department_beds = (
    ward_df.groupby("department_id")["total_beds"]
    .sum()
    .reset_index()
)

department_beds = department_beds.rename(
    columns={"total_beds": "available_beds"}
)

department_summary = department_summary.merge(
    department_beds,
    on="department_id",
    how="left"
)

department_summary["available_beds"] = (
    department_summary["available_beds"].fillna(0)
)

# Admissions per bed
department_summary["admissions_per_bed"] = (
    department_summary["total_admissions"]
    / department_summary["available_beds"].replace(0, pd.NA)
)

department_summary["admissions_per_bed"] = (
    department_summary["admissions_per_bed"].fillna(0)
)

# Normalize admission volume score between 0 and 100
max_admissions_per_bed = (
    department_summary["admissions_per_bed"].max()
)

if max_admissions_per_bed > 0:
    department_summary["admission_volume_score"] = (
        department_summary["admissions_per_bed"]
        / max_admissions_per_bed
    ) * 100
else:
    department_summary["admission_volume_score"] = 0

# Lower average LOS is considered more efficient
minimum_los = department_summary["average_los"].min()

if minimum_los > 0:
    department_summary["los_efficiency_score"] = (
        minimum_los
        / department_summary["average_los"]
    ) * 100
else:
    department_summary["los_efficiency_score"] = 0

# Weighted efficiency score
department_summary["department_efficiency_score"] = (
    0.6 * department_summary["admission_volume_score"]
    + 0.4 * department_summary["los_efficiency_score"]
)

average_department_efficiency_score = (
    department_summary["department_efficiency_score"].mean()
)

# --------------------------------------------------
# Create KPI summary table
# --------------------------------------------------

kpi_summary = pd.DataFrame({
    "KPI": [
        "Total Admissions",
        "Average Length of Stay",
        "Occupancy Rate",
        "Readmission Rate",
        "Bed Utilization Rate",
        "Average Department Efficiency Score"
    ],
    "Value": [
        total_admissions,
        round(average_los, 2),
        round(occupancy_rate, 2),
        readmission_rate,
        round(bed_utilization_rate, 2),
        round(average_department_efficiency_score, 2)
    ],
    "Unit": [
        "Admissions",
        "Days",
        "Percentage",
        "Percentage",
        "Percentage",
        "Score out of 100"
    ],
    "Validation_Status": [
        "Validated",
        "Validated",
        "Calculated using ward capacity and patient-days",
        "Not available in current dataset",
        "Calculated using registered and used beds",
        "Normalized preliminary score"
    ]
})

# --------------------------------------------------
# Save KPI outputs
# --------------------------------------------------

kpi_summary.to_csv(
    OUTPUT_DIR / "kpi_summary.csv",
    index=False
)

department_summary.to_csv(
    OUTPUT_DIR / "department_kpi_summary.csv",
    index=False
)

# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nKPI calculations completed successfully.\n")
print(kpi_summary.to_string(index=False))

print("\nAdditional validation information:")
print(f"Total available beds: {total_available_beds}")
print(f"Total registered beds: {total_registered_beds}")
print(f"Used beds: {used_beds}")
print(f"Total patient-days: {total_patient_days}")
print(f"Number of days covered: {number_of_days}")
import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
INPUT_FILE = "data/cleaned/hospital_hmis_cleaned.csv"
OUTPUT_DIR = "data/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Load cleaned HMIS dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE)

df["admission_date"] = pd.to_datetime(df["admission_date"], errors="coerce")
df["discharge_date"] = pd.to_datetime(df["discharge_date"], errors="coerce")

df["admission_day"] = df["admission_date"].dt.date
df["admission_year"] = df["admission_date"].dt.year
df["admission_month"] = df["admission_date"].dt.month
df["admission_month_name"] = df["admission_date"].dt.month_name()
df["admission_day_name"] = df["admission_date"].dt.day_name()

# -----------------------------
# 1. Hospital Overview Dataset
# Grain: One row per admission
# -----------------------------
hospital_overview_columns = [
    "admission_id",
    "patient_id",
    "admission_date",
    "discharge_date",
    "admission_type",
    "admission_status",
    "department_id",
    "department_name",
    "department_type",
    "ward_id",
    "ward_name",
    "ward_type",
    "bed_id",
    "bed_number",
    "bed_status",
    "disease_id",
    "disease_name",
    "disease_category",
    "gender",
    "date_of_birth",
    "blood_group",
    "city",
    "length_of_stay_days",
    "bill_id",
    "bill_date",
    "total_amount",
    "insurance_covered_amount",
    "patient_payable_amount",
    "payment_status",
    "payment_mode",
    "admission_year",
    "admission_month",
    "admission_month_name",
    "admission_day_name"
]

hospital_overview = df[hospital_overview_columns].copy()

hospital_overview.to_csv(
    os.path.join(OUTPUT_DIR, "hospital_overview_dataset.csv"),
    index=False
)

# -----------------------------
# 2. Patient Flow Dataset
# Grain: One row per admission event
# Note: HMIS does not contain detailed movement history.
# Therefore, admission and discharge are represented as events.
# -----------------------------
admission_events = df[
    [
        "admission_id",
        "patient_id",
        "department_id",
        "department_name",
        "ward_id",
        "ward_name",
        "bed_id",
        "admission_date",
        "admission_type",
        "admission_status"
    ]
].copy()

admission_events["movement_id"] = (
    admission_events["admission_id"].astype(str) + "_ADMISSION"
)
admission_events["movement_sequence"] = 1
admission_events["movement_type"] = "Admission"
admission_events["movement_datetime"] = admission_events["admission_date"]
admission_events["from_department"] = "External"
admission_events["current_department"] = admission_events["department_name"]
admission_events["duration_hours"] = 0

admission_events = admission_events[
    [
        "movement_id",
        "admission_id",
        "patient_id",
        "movement_sequence",
        "movement_type",
        "from_department",
        "current_department",
        "department_id",
        "ward_id",
        "ward_name",
        "bed_id",
        "movement_datetime",
        "duration_hours",
        "admission_type",
        "admission_status"
    ]
]

discharge_events = df[
    [
        "admission_id",
        "patient_id",
        "department_id",
        "department_name",
        "ward_id",
        "ward_name",
        "bed_id",
        "discharge_date",
        "length_of_stay_days",
        "admission_type",
        "admission_status"
    ]
].copy()

discharge_events["movement_id"] = (
    discharge_events["admission_id"].astype(str) + "_DISCHARGE"
)
discharge_events["movement_sequence"] = 2
discharge_events["movement_type"] = "Discharge"
discharge_events["movement_datetime"] = discharge_events["discharge_date"]
discharge_events["from_department"] = discharge_events["department_name"]
discharge_events["current_department"] = "External"
discharge_events["duration_hours"] = (
    discharge_events["length_of_stay_days"] * 24
)

discharge_events = discharge_events[
    [
        "movement_id",
        "admission_id",
        "patient_id",
        "movement_sequence",
        "movement_type",
        "from_department",
        "current_department",
        "department_id",
        "ward_id",
        "ward_name",
        "bed_id",
        "movement_datetime",
        "duration_hours",
        "admission_type",
        "admission_status"
    ]
]

patient_flow = pd.concat(
    [admission_events, discharge_events],
    ignore_index=True
)

patient_flow["movement_date"] = pd.to_datetime(
    patient_flow["movement_datetime"]
).dt.date

patient_flow["movement_year"] = pd.to_datetime(
    patient_flow["movement_datetime"]
).dt.year

patient_flow["movement_month"] = pd.to_datetime(
    patient_flow["movement_datetime"]
).dt.month

patient_flow["movement_hour"] = pd.to_datetime(
    patient_flow["movement_datetime"]
).dt.hour

patient_flow["shift"] = patient_flow["movement_hour"].apply(
    lambda hour: (
        "Morning" if 6 <= hour < 12
        else "Afternoon" if 12 <= hour < 18
        else "Evening" if 18 <= hour < 24
        else "Night"
    )
)

patient_flow.to_csv(
    os.path.join(OUTPUT_DIR, "patient_flow_dataset.csv"),
    index=False
)

# -----------------------------
# 3. Department Analytics Dataset
# Grain: One department + day
# -----------------------------
department_analytics = (
    df.groupby(
        [
            "admission_day",
            "admission_year",
            "admission_month",
            "department_id",
            "department_name",
            "department_type"
        ],
        dropna=False
    )
    .agg(
        total_admissions=("admission_id", "nunique"),
        unique_patients=("patient_id", "nunique"),
        total_beds=("total_beds", "max"),
        average_length_of_stay=("length_of_stay_days", "mean"),
        total_revenue=("total_amount", "sum"),
        average_bill_amount=("total_amount", "mean"),
        average_patient_payment=("patient_payable_amount", "mean")
    )
    .reset_index()
)

department_analytics["department_efficiency_score"] = (
    department_analytics["total_admissions"]
    / department_analytics["total_beds"].replace(0, pd.NA)
) * 100

department_analytics.to_csv(
    os.path.join(OUTPUT_DIR, "department_analytics_dataset.csv"),
    index=False
)

# -----------------------------
# 4. Resource Utilization Dataset
# Grain: One department + day + resource type
# -----------------------------
resource_base = (
    df.groupby(
        [
            "admission_day",
            "admission_year",
            "admission_month",
            "department_id",
            "department_name",
            "department_type"
        ],
        dropna=False
    )
    .agg(
        available_beds=("total_beds", "max"),
        admissions=("admission_id", "nunique"),
        occupied_beds=("bed_id", "nunique"),
        average_length_of_stay=("length_of_stay_days", "mean")
    )
    .reset_index()
)

resource_base["resource_type"] = "Beds"
resource_base["units_available"] = resource_base["available_beds"]
resource_base["units_in_use"] = resource_base["occupied_beds"]
resource_base["units_under_maintenance"] = 0
resource_base["utilization_rate"] = (
    resource_base["units_in_use"]
    / resource_base["units_available"].replace(0, pd.NA)
) * 100
resource_base["shortage_units"] = (
    resource_base["units_available"] - resource_base["units_in_use"]
)

resource_utilization = resource_base[
    [
        "admission_day",
        "admission_year",
        "admission_month",
        "department_id",
        "department_name",
        "department_type",
        "resource_type",
        "available_beds",
        "units_available",
        "units_in_use",
        "units_under_maintenance",
        "utilization_rate",
        "shortage_units",
        "admissions",
        "average_length_of_stay"
    ]
]

resource_utilization.to_csv(
    os.path.join(OUTPUT_DIR, "resource_utilization_dataset.csv"),
    index=False
)

# -----------------------------
# Validation output
# -----------------------------
print("Processed datasets created successfully.")
print(
    "Hospital Overview:",
    hospital_overview.shape
)
print(
    "Patient Flow:",
    patient_flow.shape
)
print(
    "Department Analytics:",
    department_analytics.shape
)
print(
    "Resource Utilization:",
    resource_utilization.shape
)

print("\nOutput files:")
for file_name in os.listdir(OUTPUT_DIR):
    print("-", file_name)
from pathlib import Path
import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"


# =========================================================
# LOAD ALL RAW HMIS CSV FILES
# =========================================================

tables = {}

for file in sorted(RAW_DIR.glob("*.csv")):
    tables[file.stem] = pd.read_csv(file)


# =========================================================
# DISPLAY BASIC DATASET INVENTORY
# =========================================================

print("HMIS DATA INVENTORY")
print("=" * 60)

for name, df in tables.items():
    print(f"{name}")
    print(f"  Rows    : {len(df):,}")
    print(f"  Columns : {len(df.columns)}")
    print(f"  Missing : {df.isna().sum().sum():,}")
    print("-" * 60)


# =========================================================
# BASIC DATA QUALITY VALIDATION
# =========================================================

print("\nDATA QUALITY VALIDATION")
print("=" * 60)

for name, df in tables.items():
    duplicate_rows = df.duplicated().sum()
    missing_values = df.isna().sum().sum()

    print(f"{name}")
    print(f"  Duplicate rows : {duplicate_rows:,}")
    print(f"  Missing values : {missing_values:,}")
    print("-" * 60)


# =========================================================
# HANDLE KNOWN CONDITIONAL MISSING VALUES
# =========================================================

print("\nCONDITIONAL MISSING VALUE CHECK")
print("=" * 60)

billing_detail = tables["billing_detail"]

# Room charges should have a reference ID
room_reference_present = (
    (billing_detail["charge_type"] == "Room") &
    (billing_detail["reference_id"].notna())
).sum()

# Non-room charges do not have reference IDs in this dataset
non_room_reference_missing = (
    (billing_detail["charge_type"] != "Room") &
    (billing_detail["reference_id"].isna())
).sum()

print(
    "Room charges with reference_id:",
    room_reference_present
)

print(
    "Non-room charges with missing reference_id:",
    non_room_reference_missing
)
# =========================================================
# FOREIGN-KEY INTEGRITY VALIDATION
# =========================================================

print("\nFOREIGN-KEY INTEGRITY CHECK")
print("=" * 60)


def check_relationship(child_table, child_column, parent_table, parent_column):
    child_values = tables[child_table][child_column]
    parent_values = set(tables[parent_table][parent_column])

    matched = child_values.isin(parent_values).sum()
    total = len(child_values)
    percentage = (matched / total) * 100

    print(
        f"{child_table}.{child_column} -> "
        f"{parent_table}.{parent_column}: "
        f"{percentage:.2f}% valid"
    )


check_relationship(
    "admission", "patient_id",
    "patient", "patient_id"
)

check_relationship(
    "admission", "department_id",
    "department", "department_id"
)

check_relationship(
    "admission", "ward_id",
    "ward", "ward_id"
)

check_relationship(
    "admission", "bed_id",
    "bed", "bed_id"
)

check_relationship(
    "admission", "disease_id",
    "disease", "disease_id"
)

check_relationship(
    "billing", "admission_id",
    "admission", "admission_id"
)
# =========================================================
# DATE AND LENGTH-OF-STAY VALIDATION
# =========================================================

print("\nDATE AND LENGTH-OF-STAY VALIDATION")
print("=" * 60)

admission = tables["admission"].copy()

admission["admission_date"] = pd.to_datetime(
    admission["admission_date"],
    errors="coerce"
)

admission["discharge_date"] = pd.to_datetime(
    admission["discharge_date"],
    errors="coerce"
)

# Calculate length of stay
admission["length_of_stay_days"] = (
    admission["discharge_date"]
    - admission["admission_date"]
).dt.days

invalid_dates = (
    admission["discharge_date"]
    < admission["admission_date"]
).sum()

invalid_length_of_stay = (
    admission["length_of_stay_days"] <= 0
).sum()

print("Invalid admission/discharge dates:", invalid_dates)
print("Invalid length-of-stay records:", invalid_length_of_stay)
print(
    "Average length of stay:",
    round(admission["length_of_stay_days"].mean(), 2),
    "days"
)
print(
    "Minimum length of stay:",
    admission["length_of_stay_days"].min(),
    "days"
)
print(
    "Maximum length of stay:",
    admission["length_of_stay_days"].max(),
    "days"
)
# =========================================================
# CLEANING AND TRANSFORMATION
# =========================================================

CLEANED_DIR = PROJECT_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

print("\nCLEANING AND TRANSFORMATION")
print("=" * 60)


# ---------------------------------------------------------
# Clean Admission Data
# ---------------------------------------------------------

admission_clean = tables["admission"].copy()

admission_clean["admission_date"] = pd.to_datetime(
    admission_clean["admission_date"],
    errors="coerce"
)

admission_clean["discharge_date"] = pd.to_datetime(
    admission_clean["discharge_date"],
    errors="coerce"
)

admission_clean["length_of_stay_days"] = (
    admission_clean["discharge_date"]
    - admission_clean["admission_date"]
).dt.days


# ---------------------------------------------------------
# Clean Patient Data
# ---------------------------------------------------------

patient_clean = tables["patient"].copy()

patient_clean["date_of_birth"] = pd.to_datetime(
    patient_clean["date_of_birth"],
    errors="coerce"
)


# ---------------------------------------------------------
# Save cleaned tables
# ---------------------------------------------------------

admission_clean.to_csv(
    CLEANED_DIR / "admission_cleaned.csv",
    index=False
)

patient_clean.to_csv(
    CLEANED_DIR / "patient_cleaned.csv",
    index=False
)

print("Saved: admission_cleaned.csv")
print("Saved: patient_cleaned.csv")
# =========================================================
# CLEAN AND SAVE REMAINING HMIS TABLES
# =========================================================

tables_to_clean = [
    "bed",
    "billing",
    "billing_detail",
    "department",
    "diagnostic_test",
    "disease",
    "doctor",
    "drug",
    "drug_inventory",
    "drug_manufacturer",
    "employee",
    "insurance_provider",
    "patient_diagnostic",
    "patient_insurance",
    "prescription",
    "staff_assignment",
    "ward"
]

for table_name in tables_to_clean:
    cleaned_df = tables[table_name].copy()

    cleaned_df.to_csv(
        CLEANED_DIR / f"{table_name}_cleaned.csv",
        index=False
    )

    print(f"Saved: {table_name}_cleaned.csv")
   # =========================================================
# FINAL CLEANED DATA VALIDATION
# =========================================================

print("\nFINAL CLEANED DATA VALIDATION")
print("=" * 60)

# Include all cleaned tables
all_cleaned_tables = [
    "admission",
    "patient",
    "bed",
    "billing",
    "billing_detail",
    "department",
    "diagnostic_test",
    "disease",
    "doctor",
    "drug",
    "drug_inventory",
    "drug_manufacturer",
    "employee",
    "insurance_provider",
    "patient_diagnostic",
    "patient_insurance",
    "prescription",
    "staff_assignment",
    "ward"
]

for table_name in all_cleaned_tables:

    file_path = CLEANED_DIR / f"{table_name}_cleaned.csv"
    cleaned_df = pd.read_csv(file_path)

    duplicate_rows = cleaned_df.duplicated().sum()
    missing_values = cleaned_df.isna().sum().sum()

    print(f"{table_name}")
    print(f"  Rows           : {len(cleaned_df):,}")
    print(f"  Columns        : {len(cleaned_df.columns)}")
    print(f"  Duplicate rows : {duplicate_rows:,}")

    # Special handling for billing_detail
    if table_name == "billing_detail":

        conditional_missing = (
            (cleaned_df["charge_type"] != "Room") &
            (cleaned_df["reference_id"].isna())
        ).sum()

        unexpected_missing = (
            (cleaned_df["charge_type"] == "Room") &
            (cleaned_df["reference_id"].isna())
        ).sum()

        print(
            "  Conditional missing reference_id:",
            conditional_missing
        )

        print(
            "  Unexpected missing reference_id:",
            unexpected_missing
        )

    else:
        print(f"  Missing values : {missing_values:,}")

    print("-" * 60)
    # =========================================================
# CREATE CENTRAL HMIS ANALYTICAL DATASET
# =========================================================

print("\nCREATING CENTRAL HMIS ANALYTICAL DATASET")
print("=" * 60)

# Load cleaned tables
admission_df = pd.read_csv(CLEANED_DIR / "admission_cleaned.csv")
patient_df = pd.read_csv(CLEANED_DIR / "patient_cleaned.csv")
department_df = pd.read_csv(CLEANED_DIR / "department_cleaned.csv")
ward_df = pd.read_csv(CLEANED_DIR / "ward_cleaned.csv")
bed_df = pd.read_csv(CLEANED_DIR / "bed_cleaned.csv")
disease_df = pd.read_csv(CLEANED_DIR / "disease_cleaned.csv")
billing_df = pd.read_csv(CLEANED_DIR / "billing_cleaned.csv")


# ---------------------------------------------------------
# Merge patient information
# ---------------------------------------------------------

hospital_hmis = admission_df.merge(
    patient_df,
    on="patient_id",
    how="left"
)


# ---------------------------------------------------------
# Merge department information
# ---------------------------------------------------------

hospital_hmis = hospital_hmis.merge(
    department_df,
    on="department_id",
    how="left"
)


# ---------------------------------------------------------
# Merge ward information
# ---------------------------------------------------------

hospital_hmis = hospital_hmis.merge(
    ward_df,
    on="ward_id",
    how="left",
    suffixes=("", "_ward")
)


# ---------------------------------------------------------
# Merge bed information
# ---------------------------------------------------------

hospital_hmis = hospital_hmis.merge(
    bed_df,
    on="bed_id",
    how="left",
    suffixes=("", "_bed")
)


# ---------------------------------------------------------
# Merge disease information
# ---------------------------------------------------------

hospital_hmis = hospital_hmis.merge(
    disease_df,
    on="disease_id",
    how="left"
)


# ---------------------------------------------------------
# Merge billing information
# ---------------------------------------------------------

hospital_hmis = hospital_hmis.merge(
    billing_df,
    on="admission_id",
    how="left",
    suffixes=("", "_billing")
)


# ---------------------------------------------------------
# Save central analytical dataset
# ---------------------------------------------------------

hospital_hmis.to_csv(
    CLEANED_DIR / "hospital_hmis_cleaned.csv",
    index=False
)

print(
    "Saved: hospital_hmis_cleaned.csv"
)

print(
    "Rows:",
    len(hospital_hmis)
)

print(
    "Columns:",
    len(hospital_hmis.columns)
)
# =========================================================
# CREATE CENTRAL HMIS RAW DATASET
# =========================================================

print("\nCREATING CENTRAL HMIS RAW DATASET")
print("=" * 60)

# Start from the original raw admission table
hospital_raw = tables["admission"].copy()

# Merge original raw patient data
hospital_raw = hospital_raw.merge(
    tables["patient"],
    on="patient_id",
    how="left"
)

# Merge department
hospital_raw = hospital_raw.merge(
    tables["department"],
    on="department_id",
    how="left"
)

# Merge ward
hospital_raw = hospital_raw.merge(
    tables["ward"],
    on="ward_id",
    how="left",
    suffixes=("", "_ward")
)

# Merge bed
hospital_raw = hospital_raw.merge(
    tables["bed"],
    on="bed_id",
    how="left",
    suffixes=("", "_bed")
)

# Merge disease
hospital_raw = hospital_raw.merge(
    tables["disease"],
    on="disease_id",
    how="left"
)

# Merge billing
hospital_raw = hospital_raw.merge(
    tables["billing"],
    on="admission_id",
    how="left",
    suffixes=("", "_billing")
)

# Save raw analytical dataset
hospital_raw.to_csv(
    CLEANED_DIR / "hospital_hmis_raw.csv",
    index=False
)

print("Saved: hospital_hmis_raw.csv")
print("Rows:", len(hospital_raw))
print("Columns:", len(hospital_raw.columns))
# =========================================================
# FINALIZE CENTRAL ANALYTICAL DATASETS
# =========================================================

print("\nFINALIZING CENTRAL ANALYTICAL DATASETS")
print("=" * 60)

# Columns created only because of merge operations
merge_artifact_columns = [
    "department_id_ward",
    "ward_id_bed"
]

# Remove merge artifacts
hospital_raw_final = hospital_raw.drop(
    columns=merge_artifact_columns,
    errors="ignore"
)

hospital_cleaned_final = hospital_hmis.drop(
    columns=merge_artifact_columns,
    errors="ignore"
)

# Remove contact information from analytical outputs
hospital_raw_final = hospital_raw_final.drop(
    columns=["contact_number"],
    errors="ignore"
)

hospital_cleaned_final = hospital_cleaned_final.drop(
    columns=["contact_number"],
    errors="ignore"
)

# Save final outputs
hospital_raw_final.to_csv(
    CLEANED_DIR / "hospital_hmis_raw.csv",
    index=False
)

hospital_cleaned_final.to_csv(
    CLEANED_DIR / "hospital_hmis_cleaned.csv",
    index=False
)

print("Final raw dataset:")
print("  Rows:", len(hospital_raw_final))
print("  Columns:", len(hospital_raw_final.columns))

print("Final cleaned dataset:")
print("  Rows:", len(hospital_cleaned_final))
print("  Columns:", len(hospital_cleaned_final.columns))

print(
    "Cleaned derived columns:",
    [
        col for col in hospital_cleaned_final.columns
        if col not in hospital_raw_final.columns
    ]
)
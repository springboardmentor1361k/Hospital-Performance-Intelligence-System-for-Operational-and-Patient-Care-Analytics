
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT DIRECTORIES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "hospital_data"
OUTPUT_DIR = BASE_DIR / "cleaned_hospital_data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD ORIGINAL DATASETS
# --------------------------------------------------

data = {}

for file_path in DATA_DIR.glob("*.csv"):
    table_name = file_path.stem
    data[table_name] = pd.read_csv(file_path)

if not data:
    raise FileNotFoundError(
        f"No CSV files found in: {DATA_DIR}"
    )

print(f"Loaded {len(data)} hospital datasets.")

# --------------------------------------------------
# 3. CLEAN EACH DATASET
# --------------------------------------------------

for table_name, df in data.items():
    print(f"\nProcessing: {table_name}")
    rows_before = len(df)

    # Remove exact duplicate rows
    df = df.drop_duplicates().copy()
    duplicates_removed = rows_before - len(df)

    # Standardize ID fields without converting missing IDs to text
    id_cols = [
        col for col in df.columns
        if col.lower().endswith("_id")
        or col.lower() in ["id", "policy_number"]
    ]

    for col in id_cols:
        values = df[col].astype("string").str.strip()
        values = values.str.replace(r"\.0$", "", regex=True)
        values = values.replace(
            r"(?i)^(nan|none|null|<na>)$",
            pd.NA,
            regex=True
        )
        df[col] = values

    # Clean text fields
    text_cols = df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    for col in text_cols:
        if col in id_cols:
            continue

        values = df[col].astype("string").str.strip()
        values = values.replace(
            r"(?i)^(nan|none|null|<na>)$",
            pd.NA,
            regex=True
        )

        if col.lower() == "blood_group":
            values = values.str.upper()
        elif col.lower() in ["icu", "room_no"]:
            values = values.str.upper()
        else:
            values = values.str.title()

        df[col] = values

    # Report missing values; don't guess replacements for numeric fields
    missing_count = int(df.isna().sum().sum())

    # Save with the existing *_clean.csv naming convention
    output_path = OUTPUT_DIR / f"{table_name}_clean.csv"
    df.to_csv(output_path, index=False)

    print(f"Original rows: {rows_before}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Missing cells remaining: {missing_count}")
    print(f"Saved: {output_path}")

print("\nMilestone 1 cleaning completed.")
print(f"Cleaned files location: {OUTPUT_DIR}")
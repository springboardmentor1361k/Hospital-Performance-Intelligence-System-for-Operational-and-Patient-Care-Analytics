
import pandas as pd
from pathlib import Path

# Folder containing this Python file
DATA = Path(__file__).parent

# Get all CSV files in this folder
files = [
    f for f in DATA.glob("*.csv")
    if not f.name.startswith("member5_")
]

summary = []
missing_details = []

for file in files:
    df = pd.read_csv(file)
    
    if file.name == "billing_detail.csv":
        print("\n--- REFERENCE ID CHECK ---")
        print(df["reference_id"].isnull().value_counts())

        print("\nMissing reference_id by charge_type:")
        print(
            df.groupby("charge_type")["reference_id"]
            .apply(lambda x: x.isnull().sum())
        )

        print("\nSample rows with missing reference_id:")
        print(
            df[df["reference_id"].isnull()]
            [["billing_detail_id", "bill_id", "charge_type", "reference_id", "amount"]]
            .head(10)
        )

    # Row count and column count
    rows, columns = df.shape

    # Missing values
    missing = df.isnull().sum()

    # Complete duplicate rows
    duplicates = df.duplicated().sum()

    summary.append({
        "Dataset": file.name,
        "Rows": rows,
        "Columns": columns,
        "Total_Missing_Values": int(missing.sum()),
        "Duplicate_Rows": int(duplicates)
    })

    for column, count in missing.items():
        if count > 0:
            missing_details.append({
                "Dataset": file.name,
                "Column": column,
                "Missing_Values": int(count)
            })

    print(f"\nDataset: {file.name}")
    print(f"Rows: {rows}")
    print(f"Columns: {columns}")
    print(f"Missing values: {missing.sum()}")
    print(f"Duplicate rows: {duplicates}")

# Save reports
pd.DataFrame(summary).to_csv(
    DATA / "member5_testing_summary.csv", index=False
)

pd.DataFrame(missing_details).to_csv(
    DATA / "member5_missing_details.csv", index=False
)

print("\nTesting completed!")
print("Reports saved successfully.")

import pandas as pd
from pathlib import Path

# Project folder
BASE_DIR = Path(__file__).resolve().parent

# Input dataset
DATA_FILE = BASE_DIR / "Data" / "cleaned" / "hospital_cleaned.csv"

# Output files
EXCEL_FILE = BASE_DIR / "hospital_final_dataset.xlsx"
KPI_FILE = BASE_DIR / "hospital_kpi_summary.csv"


def main():
    # Load hospital data
    df = pd.read_csv(DATA_FILE)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
    df["Length_of_Stay"] = pd.to_numeric(
        df["Length_of_Stay"], errors="coerce"
    )
    df["Satisfaction"] = pd.to_numeric(
        df["Satisfaction"], errors="coerce"
    )

    # Calculate KPIs from the dataset
    total_patients = len(df)
    total_cost = df["Cost"].sum()
    average_cost = df["Cost"].mean()
    average_stay = df["Length_of_Stay"].mean()
    average_satisfaction = df["Satisfaction"].mean()

    readmission_counts = (
        df["Readmission"].astype(str).str.strip().str.lower()
    )
    readmission_rate = (
        readmission_counts.eq("yes").mean() * 100
        if total_patients > 0 else 0
    )

    # Prepare KPI summary
    kpis = [
        ["Total Patient Records", total_patients],
        ["Total Treatment Cost", round(total_cost, 2)],
        ["Average Treatment Cost", round(average_cost, 2)],
        ["Average Length of Stay (Days)", round(average_stay, 2)],
        ["Readmission Rate (%)", round(readmission_rate, 2)],
        ["Average Patient Satisfaction", round(average_satisfaction, 2)]
    ]

    kpi_df = pd.DataFrame(kpis, columns=["KPI", "Value"])

    # Save final dataset and KPI summary
    df.to_excel(EXCEL_FILE, index=False)
    kpi_df.to_csv(KPI_FILE, index=False)

    # Display results
    print("\nHOSPITAL KPI SUMMARY")
    print("=" * 40)

    for name, value in kpis:
        print(f"{name}: {value}")

    print("\nFiles created successfully:")
    print(EXCEL_FILE)
    print(KPI_FILE)


if __name__ == "__main__":
    main()
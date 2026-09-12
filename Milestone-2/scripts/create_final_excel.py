import pandas as pd
from pathlib import Path

output_path = Path("Milestone-2/hospital_final_dataset.xlsx")

datasets = {
    "Hospital Overview": "data/processed/hospital_overview_dataset.csv",
    "Patient Flow": "data/processed/patient_flow_dataset.csv",
    "Department Analytics": "data/processed/department_analytics_dataset.csv",
    "Resource Utilization": "data/processed/resource_utilization_dataset.csv",
    "KPI Summary": "data/processed/kpi_summary.csv",
    "Department KPI Summary": "data/processed/department_kpi_summary.csv",
}

with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
    for sheet_name, file_path in datasets.items():
        df = pd.read_csv(file_path)
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

print(f"Final Excel dataset created successfully: {output_path}")
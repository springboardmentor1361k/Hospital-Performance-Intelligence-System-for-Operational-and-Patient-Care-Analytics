MedTrack_DV – Clean 500-Row Synthetic Dataset

IMPORTANT:
This is a purpose-built SYNTHETIC dataset created for the MedTrack hospital analytics
dashboard project. It is not a real hospital/public dataset and should be labelled as synthetic
data in project documentation.

Each CSV contains exactly 500 rows and is designed around the four analytical grains in the
MedTrack guidance document.

Files:
1. hospital_overview_dataset.csv – 500 admissions
2. patient_flow_dataset.csv – 500 movement events
3. department_analytics_dataset.csv – 500 department-day records
4. resource_utilization_dataset.csv – 500 resource records
5. dataset_dictionary.csv – grain and purpose summary

Common linking keys:
hospital_id, department_id, patient_id, admission_id, date (where applicable)

The data contains no blank cells, exact duplicate rows, negative billing amounts, or impossible
percentage values. Dates are in ISO format (YYYY-MM-DD), and IDs are standardized.

Use the four CSVs as separate logical tables in Tableau rather than blindly joining all rows.

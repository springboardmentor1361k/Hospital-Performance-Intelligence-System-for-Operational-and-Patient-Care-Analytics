# Data Cleaning Report

## Hospital Performance Intelligence System

---

## 1. Purpose

This report documents the data cleaning and preprocessing activities performed on the Core HMIS dataset used in the Hospital Performance Intelligence System.

The objective of cleaning was to improve data quality, maintain consistency and prepare reliable datasets for analysis and visualization.

---

## 2. Source Dataset

The Core HMIS dataset contains hospital information related to:

- Patient admissions
- Patient details
- Departments
- Wards
- Beds
- Diseases
- Billing
- Doctors and staff
- Prescriptions
- Diagnostic tests
- Insurance details

The raw datasets were preserved in the `data/raw` directory.

---

## 3. Cleaning Activities Performed

### 3.1 Missing Value Check

Missing values were checked across all cleaned tables.

The main analytical dataset was checked for missing values in required fields such as:

- Admission ID
- Patient ID
- Admission date
- Discharge date
- Department ID
- Ward ID
- Length of stay

No missing values were found in the required fields of the final analytical dataset.

### 3.2 Duplicate Record Check

Duplicate records and duplicate admission IDs were checked.

- Duplicate admission IDs: 0
- Duplicate records in the final analytical dataset: 0

### 3.3 Date Validation

Admission and discharge dates were checked for consistency.

The following validations were performed:

- Admission dates were converted into a consistent date format.
- Discharge dates were converted into a consistent date format.
- Discharge dates were checked to ensure they were not earlier than admission dates.

### 3.4 Length of Stay Validation

Length of stay was checked for invalid, negative and missing values.

- Minimum length of stay: 1 day
- Maximum length of stay: 15 days
- Invalid length-of-stay values: 0
- Average length of stay: 5.16 days

### 3.5 Referential Integrity Check

Foreign-key relationships were checked between related tables.

The following relationships were validated:

- Admission to patient
- Admission to department
- Admission to ward
- Admission to bed
- Admission to disease

All checked relationships were valid.

### 3.6 Data Type Standardization

Data types were standardized for analysis.

Examples include:

- Dates converted to date format
- Numerical fields converted to numeric format
- IDs retained as consistent identifiers
- Categorical fields retained as text values

### 3.7 Dataset Integration

The cleaned Core HMIS tables were joined using validated identifiers.

The main analytical dataset was created at the admission level, with one row representing one hospital admission.

The following datasets were created:

- `hospital_overview_dataset.csv`
- `patient_flow_dataset.csv`
- `department_analytics_dataset.csv`
- `resource_utilization_dataset.csv`

---

## 4. Cleaning Validation Summary

| Validation Check | Result |
|---|---|
| Required fields with missing values | 0 |
| Duplicate admission IDs | 0 |
| Invalid length-of-stay values | 0 |
| Invalid admission-discharge date relationships | 0 |
| Invalid patient references | 0 |
| Invalid department references | 0 |
| Invalid ward references | 0 |
| Invalid bed references | 0 |
| Invalid disease references | 0 |

---

## 5. Data Preservation

The raw datasets were not modified during cleaning.

The project follows the following structure:

```text
data/
├── raw/
├── cleaned/
└── processed/
```

- `data/raw` contains the original source files.
- `data/cleaned` contains cleaned and standardized tables.
- `data/processed` contains analytical datasets prepared for KPI calculation and Tableau visualization.

---

## 6. Limitations

- The current cleaning process is primarily based on the Core HMIS dataset.
- Some approved external datasets have not yet been integrated.
- Readmission-related information is not available in the current Core HMIS dataset.
- Bed utilization is currently calculated using beds associated with admission records.
- Further cleaning and validation may be required after integrating the remaining approved datasets.

---

## 7. Conclusion

The cleaning process produced consistent and analysis-ready datasets for hospital operational and patient-care analytics.

The cleaned datasets were validated for duplicates, missing values, date consistency, length of stay and referential integrity. The processed datasets are now ready for KPI calculation and Tableau dashboard development.
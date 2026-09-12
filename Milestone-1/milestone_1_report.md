# Milestone 1 Report

## Hospital Performance Intelligence System

---

## 1. Introduction

The Hospital Performance Intelligence System is designed to analyse hospital operations, patient flow, department performance and resource utilization.

The project uses a Core Hospital Management Information System dataset as the primary source. The data was cleaned, validated and transformed into analytical datasets suitable for KPI calculation and future Tableau visualization.

---

## 2. Objectives

The objectives of Milestone 1 are:

- Select an appropriate hospital dataset.
- Collect and preserve raw data.
- Perform data inventory and quality analysis.
- Validate missing values and duplicate records.
- Validate foreign-key relationships.
- Validate dates and length of stay.
- Clean and standardize the data.
- Create analytical datasets.
- Define the grain of each analytical dataset.
- Prepare the data model for KPI analysis and Tableau.

---

## 3. Dataset Selection

The selected core dataset is:

**Hospital HMIS Dataset for Healthcare Analytics**

The dataset contains operational, patient, department, ward, bed, disease, billing and clinical information.

The following tables were used:

- Admission
- Patient
- Department
- Ward
- Bed
- Disease
- Billing
- Billing Detail
- Doctor
- Employee
- Prescription
- Diagnostic Test
- Patient Diagnostic
- Patient Insurance
- Insurance Provider
- Drug
- Drug Inventory
- Drug Manufacturer
- Staff Assignment

---

## 4. Data Collection

The raw HMIS data was collected and preserved in the project repository.

Raw data location:

`data/raw/`

The original raw files were not modified.

Cleaned data location:

`data/cleaned/`

Processed analytical data location:

`data/processed/`

---

## 5. Data Inventory

| Table | Rows | Columns |
|---|---:|---:|
| Admission | 45,000 | 10 |
| Patient | 30,000 | 6 |
| Department | 11 | 5 |
| Ward | 27 | 5 |
| Bed | 415 | 4 |
| Billing | 45,000 | 8 |
| Billing Detail | 112,402 | 5 |
| Diagnostic Test | 9 | 5 |
| Disease | 20 | 3 |
| Doctor | 98 | 5 |
| Drug | 250 | 6 |
| Drug Inventory | 250 | 6 |
| Drug Manufacturer | 300 | 5 |
| Employee | 500 | 7 |
| Insurance Provider | 50 | 5 |
| Patient Diagnostic | 63,269 | 6 |
| Patient Insurance | 21,617 | 7 |
| Prescription | 73,109 | 6 |
| Staff Assignment | 207 | 4 |

---

## 6. Data Quality Validation

### 6.1 Missing-Value Analysis

Missing-value analysis was performed on the core HMIS tables.

The cleaned analytical admission dataset contains no missing values in the required analytical fields.

The billing detail table contains missing reference identifiers for some non-room billing charges. These values were treated as structurally unavailable rather than incorrectly filled.

---

### 6.2 Duplicate Checking

Duplicate checking was performed on the collected HMIS tables.

Result:

- Duplicate records found: 0
- Duplicate admission identifiers: 0
- Duplicate patient identifiers: 0 in the patient master table

**Status: Passed**

---

### 6.3 Foreign-Key Validation

The following relationships were validated:

| Relationship | Result |
|---|---|
| Admission to Patient | 100% valid |
| Admission to Department | 100% valid |
| Admission to Ward | 100% valid |
| Admission to Bed | 100% valid |
| Admission to Disease | 100% valid |
| Billing to Admission | 100% valid |

**Status: Passed**

---

### 6.4 Date Validation

The following date fields were checked:

- Admission date
- Discharge date
- Billing date
- Date of birth

Invalid or inconsistent date records were not found in the cleaned analytical admission dataset.

**Status: Passed**

---

### 6.5 Length-of-Stay Validation

Length of stay was checked using admission and discharge dates.

Validation results:

- Invalid length-of-stay records: 0
- Minimum length of stay: 1 day
- Maximum length of stay: 15 days
- Average length of stay: 5.16 days

**Status: Passed**

---

## 7. Data Cleaning Activities

The following cleaning activities were completed:

- Standardized column names.
- Converted date fields to valid date formats.
- Removed duplicate records.
- Validated primary and foreign keys.
- Checked missing values.
- Validated admission and discharge dates.
- Validated length-of-stay values.
- Standardized data types.
- Joined related HMIS tables using valid keys.
- Preserved raw data separately from cleaned data.

---

## 8. Analytical Datasets Created

Four analytical datasets were created in the processed data folder.

### 8.1 Hospital Overview Dataset

**File:**  
`data/processed/hospital_overview_dataset.csv`

**Grain:**  
One row per admission.

**Rows:**  
45,000

**Purpose:**

- Total admissions
- Average length of stay
- Patient demographics
- Disease analysis
- Department analysis
- Billing analysis

---

### 8.2 Patient Flow Dataset

**File:**  
`data/processed/patient_flow_dataset.csv`

**Grain:**  
One row per patient movement event.

**Event types:**

- Admission
- Discharge

**Rows:**  
90,000

**Purpose:**

- Admission trends
- Discharge trends
- Patient movement analysis
- Daily patient flow analysis

---

### 8.3 Department Analytics Dataset

**File:**  
`data/processed/department_analytics_dataset.csv`

**Grain:**  
One department per day.

**Rows:**  
12,474

**Purpose:**

- Department performance
- Admission and discharge comparison
- Average length-of-stay analysis
- Revenue analysis
- Department efficiency analysis

---

### 8.4 Resource Utilization Dataset

**File:**  
`data/processed/resource_utilization_dataset.csv`

**Grain:**  
One department per day per resource type.

**Rows:**  
12,474

**Purpose:**

- Bed utilization
- Occupancy analysis
- Resource planning
- Department capacity analysis

---

## 9. Data Model

The main entities in the data model are:

- Patient
- Admission
- Department
- Ward
- Bed
- Disease
- Billing

The primary relationship is:

`Patient → Admission → Department/Ward/Bed/Disease/Billing`

The analytical datasets were created at different grains to prevent duplication and double-counting.

---

## 10. Relationship Validation

The analytical datasets were validated based on their defined grains.

The following relationships are supported:

| Dataset | Relationship |
|---|---|
| Hospital Overview to Patient Flow | admission_id |
| Hospital Overview to Department Analytics | department_id |
| Department Analytics to Resource Utilization | department_id |
| Department to Department Analytics | department_id |
| Department to Resource Utilization | department_id |

Relationships must be handled carefully because daily datasets and admission-level datasets have different grains.

---

## 11. Dataset Limitations

The following limitations were identified:

1. The current HMIS dataset does not contain a reliable readmission indicator.
2. The current bed data supports preliminary bed assignment utilization.
3. Daily bed occupancy requires daily census or bed movement records.
4. The remaining approved datasets must be collected and validated before final integration.
5. Datasets without compatible keys will be maintained separately.
6. The processed datasets are initially based on the Core HMIS dataset.

---

## 12. Milestone 1 Deliverables

The following Milestone 1 deliverables have been completed:

- Core HMIS dataset selection
- Raw HMIS data collection
- Data inventory
- Missing-value analysis
- Duplicate checking
- Foreign-key validation
- Date validation
- Length-of-stay validation
- HMIS cleaning
- Raw and cleaned data preservation
- Four processed analytical datasets
- Dataset grain definitions
- Dataset validation and mapping sheet
- Data model documentation
- Milestone 1 report

---

## 13. Conclusion

The Core HMIS dataset was successfully collected, cleaned and validated.

Four analytical datasets were created with clearly defined grains for hospital overview, patient flow, department analytics and resource utilization.

The resulting data model provides a reliable foundation for KPI calculation and Tableau dashboard development in Milestone 2.

The remaining approved datasets will be collected and validated before finalizing readmission, bed-management and discharge-specific analysis.
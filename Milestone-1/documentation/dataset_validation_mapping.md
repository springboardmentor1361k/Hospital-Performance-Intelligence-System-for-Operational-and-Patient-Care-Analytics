# Dataset Validation and Mapping Sheet

## 1. Purpose

This document records the approved datasets used in the Hospital Performance Intelligence System. It defines the role, grain, important fields, join keys, validation status, and integration approach for each dataset.

The datasets are not blindly merged. Each dataset is used according to its business purpose and available keys.

---

## 2. Approved Dataset Summary

| Dataset | Role | Usage | Integration Status |
|---|---|---|---|
| Hospital HMIS Dataset for Healthcare Analytics | Core dataset | Admissions, patients, departments, wards, beds, billing and clinical information | Selected as the primary dataset |
| Hospital Beds Management | Resource dataset | Bed availability, occupancy and resource utilization | To be collected and validated |
| Hospital Data for Patient Readmission Prediction | Patient outcome dataset | Readmission-related analysis | To be collected and validated |
| Hospital Inpatient Discharges Dataset | Inpatient/discharge dataset | Discharge trends and inpatient outcomes | To be collected and validated |

---

## 3. Core HMIS Dataset

### Dataset Name

Hospital HMIS Dataset for Healthcare Analytics

### Dataset Role

Core operational and patient-care dataset.

### Main Tables

- admission
- patient
- department
- ward
- bed
- disease
- billing
- billing_detail
- doctor
- employee
- prescription
- diagnostic_test
- patient_diagnostic
- patient_insurance
- insurance_provider
- drug
- drug_inventory
- drug_manufacturer
- staff_assignment

### Main Analytical Grain

One row per hospital admission in the Hospital Overview dataset.

### Important Keys

| Key | Description |
|---|---|
| admission_id | Unique admission identifier |
| patient_id | Identifies the patient |
| department_id | Identifies the department |
| ward_id | Identifies the ward |
| bed_id | Identifies the assigned bed |
| disease_id | Identifies the disease or diagnosis |
| bill_id | Identifies the billing record |

### Important Fields

| Field | Purpose |
|---|---|
| admission_date | Admission date |
| discharge_date | Discharge date |
| admission_type | Type of admission |
| admission_status | Current admission status |
| length_of_stay_days | Duration of hospital stay |
| department_name | Department analysis |
| ward_name | Ward analysis |
| total_beds | Available ward capacity |
| bed_status | Bed status |
| total_amount | Total bill amount |
| insurance_covered_amount | Insurance-covered amount |
| patient_payable_amount | Amount payable by patient |
| payment_status | Payment status |
| gender | Patient demographic analysis |
| city | Patient location analysis |
| disease_name | Disease analysis |

---

## 4. Core HMIS Validation Results

| Validation Check | Result | Status |
|---|---:|---|
| Total admissions | 45,000 | Passed |
| Total patients | 30,000 | Passed |
| Duplicate records | 0 | Passed |
| Invalid admission dates | 0 | Passed |
| Invalid discharge dates | 0 | Passed |
| Invalid length-of-stay values | 0 | Passed |
| Invalid patient foreign keys | 0 | Passed |
| Invalid department foreign keys | 0 | Passed |
| Invalid ward foreign keys | 0 | Passed |
| Invalid bed foreign keys | 0 | Passed |
| Invalid disease foreign keys | 0 | Passed |
| Invalid billing admission keys | 0 | Passed |
| Average length of stay | 5.16 days | Passed |

---

## 5. Dataset Grain Mapping

| Analytical Dataset | Grain | Main Purpose |
|---|---|---|
| hospital_overview_dataset.csv | One row per admission | Overall hospital performance analysis |
| patient_flow_dataset.csv | One row per patient movement event | Admission and discharge flow analysis |
| department_analytics_dataset.csv | One hospital + department + day | Department-level performance analysis |
| resource_utilization_dataset.csv | One hospital + department + day + resource type | Bed and resource utilization analysis |

---

## 6. Analytical Dataset Mapping

### Hospital Overview Dataset

**File:**

`data/processed/hospital_overview_dataset.csv`

**Grain:** One row per admission.

**Main fields:**

- admission_id
- admission_date
- discharge_date
- patient_id
- department_id
- department_name
- ward_id
- bed_id
- disease_id
- length_of_stay_days
- total_amount
- insurance_covered_amount
- patient_payable_amount
- admission_type
- admission_status

**Purpose:**

Used for total admissions, average length of stay, patient demographics, disease analysis and financial analysis.

---

### Patient Flow Dataset

**File:**

`data/processed/patient_flow_dataset.csv`

**Grain:** One row per patient movement event.

**Event types:**

- Admission
- Discharge

**Main fields:**

- admission_id
- patient_id
- department_id
- department_name
- ward_id
- bed_id
- event_date
- event_type
- length_of_stay_days

**Purpose:**

Used to analyse admission trends, discharge trends, patient movement and patient flow over time.

---

### Department Analytics Dataset

**File:**

`data/processed/department_analytics_dataset.csv`

**Grain:** One department per day.

**Main fields:**

- department_id
- department_name
- date
- total_admissions
- total_discharges
- average_length_of_stay
- total_patient_days
- total_revenue
- average_revenue_per_admission

**Purpose:**

Used for department comparison, department efficiency and operational performance analysis.

---

### Resource Utilization Dataset

**File:**

`data/processed/resource_utilization_dataset.csv`

**Grain:** One department per day per resource type.

**Resource types:**

- Beds
- Patient-days
- Admissions

**Main fields:**

- department_id
- department_name
- date
- resource_type
- available_capacity
- utilized_amount
- utilization_rate

**Purpose:**

Used for bed utilization, occupancy analysis and resource planning.

---

## 7. Join and Relationship Mapping

| Parent Dataset/Table | Child Dataset/Table | Join Key | Relationship |
|---|---|---|---|
| patient | admission | patient_id | One patient can have multiple admissions |
| department | admission | department_id | One department can have multiple admissions |
| ward | admission | ward_id | One ward can have multiple admissions |
| bed | admission | bed_id | One bed can be assigned to multiple admissions over time |
| disease | admission | disease_id | One disease can be associated with multiple admissions |
| admission | billing | admission_id | One admission can have one billing record |
| admission | patient_flow_dataset | admission_id | One admission can have multiple movement events |
| department | department_analytics_dataset | department_id | One department has multiple daily records |
| department | resource_utilization_dataset | department_id | One department has multiple daily resource records |

---

## 8. Integration Rules

1. The core HMIS dataset is used as the primary operational dataset.
2. The four approved datasets are not blindly appended together.
3. Datasets are joined only when a valid common key is available.
4. Datasets without compatible keys are kept as separate analytical sources.
5. Raw datasets are preserved without modification.
6. Cleaned datasets are stored separately.
7. Processed analytical datasets are stored in `data/processed`.
8. Readmission analysis will only be performed after validating the readmission dataset.
9. Bed utilization analysis will be validated against the approved Hospital Beds Management dataset when it is collected.
10. Dataset limitations are documented rather than hidden.

---

## 9. Current Integration Status

| Dataset | Current Status |
|---|---|
| Core HMIS dataset | Collected, cleaned and processed |
| Hospital Beds Management | Pending collection and validation |
| Hospital Readmission Dataset | Pending collection and validation |
| Hospital Inpatient Discharges Dataset | Pending collection and validation |

---

## 10. Data Quality Conclusion

The core HMIS dataset passed duplicate, missing-value, foreign-key, date and length-of-stay validation checks.

The core dataset is suitable for creating the initial analytical datasets and calculating preliminary operational KPIs.

The remaining approved datasets must be collected and validated before finalizing readmission, bed-management and discharge-specific analysis.
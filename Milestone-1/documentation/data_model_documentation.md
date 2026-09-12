# Data Model Documentation

## 1. Project Overview

The Hospital Performance Intelligence System uses cleaned and processed hospital datasets to analyse hospital operations, patient flow, department performance and resource utilization.

The Core HMIS dataset acts as the primary operational source. Additional approved datasets will be validated and integrated only when compatible keys and business meanings are available.

---

## 2. Data Architecture

The project follows a three-layer data architecture:

1. Raw Layer
2. Cleaned Layer
3. Processed Analytical Layer

### Raw Layer

Location:

`data/raw/`

The raw layer contains the original downloaded datasets. These files are preserved without modification.

### Cleaned Layer

Location:

`data/cleaned/`

The cleaned layer contains datasets after:

- Missing-value analysis
- Duplicate checking
- Date validation
- Length-of-stay validation
- Foreign-key validation
- Data-type correction
- Standardization of column values

### Processed Layer

Location:

`data/processed/`

The processed layer contains analytical datasets prepared for KPI calculations and Tableau visualization.

---

## 3. Core HMIS Data Model

The Core HMIS dataset contains the following major entities:

- Patient
- Admission
- Department
- Ward
- Bed
- Disease
- Billing
- Prescription
- Diagnostic Test
- Insurance Provider
- Employee
- Doctor

---

## 4. Entity Relationships

### Patient to Admission

One patient can have multiple admissions.

Relationship:

`patient.patient_id → admission.patient_id`

Cardinality:

One-to-many

---

### Department to Admission

One department can have multiple admissions.

Relationship:

`department.department_id → admission.department_id`

Cardinality:

One-to-many

---

### Ward to Admission

One ward can be associated with multiple admissions.

Relationship:

`ward.ward_id → admission.ward_id`

Cardinality:

One-to-many

---

### Bed to Admission

One bed can be assigned to multiple admissions over different periods.

Relationship:

`bed.bed_id → admission.bed_id`

Cardinality:

One-to-many over time

---

### Disease to Admission

One disease can be associated with multiple admissions.

Relationship:

`disease.disease_id → admission.disease_id`

Cardinality:

One-to-many

---

### Admission to Billing

An admission can have a billing record.

Relationship:

`admission.admission_id → billing.admission_id`

Cardinality:

One-to-one or one-to-many depending on billing detail records

---

## 5. Analytical Dataset Model

### Hospital Overview Dataset

File:

`data/processed/hospital_overview_dataset.csv`

Grain:

One row per admission.

Primary identifier:

`admission_id`

Purpose:

- Total admissions
- Average length of stay
- Patient demographics
- Disease analysis
- Department comparison
- Billing analysis

---

### Patient Flow Dataset

File:

`data/processed/patient_flow_dataset.csv`

Grain:

One row per patient movement event.

Event types:

- Admission
- Discharge

Important fields:

- admission_id
- patient_id
- department_id
- department_name
- ward_id
- bed_id
- event_date
- event_type
- length_of_stay_days

Purpose:

- Admission trends
- Discharge trends
- Patient movement
- Daily patient flow

---

### Department Analytics Dataset

File:

`data/processed/department_analytics_dataset.csv`

Grain:

One department per day.

Important fields:

- department_id
- department_name
- date
- total_admissions
- total_discharges
- average_length_of_stay
- total_patient_days
- total_revenue
- average_revenue_per_admission

Purpose:

- Department performance
- Department efficiency
- Admission and discharge comparison
- Revenue comparison

---

### Resource Utilization Dataset

File:

`data/processed/resource_utilization_dataset.csv`

Grain:

One department per day per resource type.

Resource types:

- Beds
- Patient-days
- Admissions

Purpose:

- Bed utilization analysis
- Occupancy analysis
- Resource planning
- Department capacity comparison

---

## 6. KPI Data Sources

| KPI | Primary Dataset | Main Fields |
|---|---|---|
| Total Admissions | Hospital Overview | admission_id |
| Average Length of Stay | Hospital Overview | length_of_stay_days |
| Occupancy Rate | Hospital Overview and Ward | length_of_stay_days, total_beds |
| Readmission Rate | Approved readmission dataset | patient_id, readmission indicator |
| Bed Utilization Rate | Hospital Overview and Bed | bed_id |
| Department Efficiency Score | Department Analytics | admissions, average LOS and department capacity |

---

## 7. Tableau Data Model

The recommended Tableau model uses the following structure:

### Main Analytical Tables

- Hospital Overview
- Patient Flow
- Department Analytics
- Resource Utilization

### Recommended Relationships

| Table 1 | Table 2 | Relationship Field |
|---|---|---|
| Hospital Overview | Patient Flow | admission_id |
| Hospital Overview | Department Analytics | department_id |
| Department Analytics | Resource Utilization | department_id |
| Hospital Overview | Resource Utilization | department_id |

Relationships should be created only when the grain and relationship cardinality are understood.

The Hospital Overview dataset should not be directly joined to daily datasets without considering duplication risk. Tableau relationships or separate data sources are preferred over careless physical joins.

---

## 8. Data Grain and Duplication Control

Each analytical dataset has a defined grain:

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per admission |
| Patient Flow | One row per movement event |
| Department Analytics | One department per day |
| Resource Utilization | One department per day per resource type |

When combining datasets, the project must avoid:

- Duplicate admissions
- Double-counted patient-days
- Repeated revenue values
- Inflated bed capacity
- Incorrect department totals

---

## 9. Data Quality Controls

The following checks are applied before analysis:

- Duplicate record checking
- Missing-value analysis
- Foreign-key validation
- Date validation
- Length-of-stay validation
- Primary-key uniqueness checking
- Data-type validation
- Relationship validation
- Aggregation-level validation

---

## 10. Data Model Limitations

1. The current HMIS dataset does not provide a reliable readmission indicator.
2. The current bed data supports preliminary bed assignment utilization.
3. Daily bed occupancy requires reliable bed movement or daily census data.
4. The approved external datasets must be validated before integration.
5. Datasets without compatible keys will be maintained as separate analytical sources.

---

## 11. Conclusion

The data model separates operational, patient-flow, department and resource-level analysis.

This structure reduces duplication risk and supports reliable KPI calculations, Tableau relationships and future integration of the remaining approved datasets.
# MedTrack_DV — Dataset Sources & Data Documentation

## 1. Overview

MedTrack_DV uses healthcare-related source datasets to construct four analytical datasets covering:

- Hospital admissions
- Patient movement
- Department performance
- Resource utilization

The project guidance emphasizes that datasets should not be blindly merged because the four analytical datasets have different grains.

## 2. Approved Source Dataset Stack

| Source Dataset | Role | Main Use |
|---|---|---|
| Hospital HMIS Dataset for Healthcare Analytics | Core hospital dataset | Hospital operations, admissions, departments, patients, beds and staff |
| Hospital Beds Management | Resource and capacity dataset | Beds, staffing, capacity and service demand |
| Hospital Data for Patient Readmission Prediction | Patient/outcome dataset | Readmissions, LOS, discharge and patient outcomes |
| Hospital Inpatient Discharges Dataset | Inpatient/discharge dataset | Admissions, discharges, LOS and inpatient analysis |

## 3. Hospital HMIS Dataset

**Role:** Core Hospital Dataset

Used for:

- Hospital Overview
- Patient Flow
- Department Analytics
- Resource Utilization
- Admissions
- Discharges
- Departments
- Wards
- Beds
- Patients
- Staff
- Doctors

**Source:** Kaggle — Hospital HMIS Dataset for Healthcare Analytics

## 4. Hospital Beds Management

**Role:** Resource and Capacity Dataset

Used for:

- Available beds
- Bed capacity
- Staff allocation
- Staff availability
- Service demand
- Resource trends
- Capacity planning
- Patient satisfaction

**Source:** Kaggle — Hospital Beds Management

## 5. Hospital Data for Patient Readmission Prediction

**Role:** Patient and Outcome Dataset

Used for:

- Readmission analysis
- Length of stay
- Discharge analysis
- Patient flow
- Patient demographics
- Occupied vs available beds
- Patient outcomes

**Source:** Kaggle — Hospital Data for Patient Readmission Prediction

## 6. Hospital Inpatient Discharges Dataset

**Role:** Inpatient and Discharge Dataset

Used for:

- Admission patterns
- Discharge patterns
- Length of stay
- Inpatient volume
- Patient demographics
- Hospital operational comparisons

**Source:** Kaggle — Hospital Inpatient Discharges Dataset

## 7. Final Analytical Datasets

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per hospital admission |
| Patient Flow | One row per patient movement event |
| Department Analytics | One row per hospital + department + day |
| Resource Utilization | One row per hospital + department + date + resource type |

## 8. Data Quality Requirements

The project guidance specifies:

- Dataset completeness above 95%
- Less than 2% missing values after cleaning
- Correct KPI calculations
- Standardized identifiers
- Standardized dates
- Valid relationships
- Documented dataset grain

## 9. Data Modeling Principle

The four analytical datasets have different grains and should not be blindly joined into one large table.

Common keys include:

- Hospital ID
- Department ID
- Patient ID
- Admission ID
- Date

## 10. Related Documentation

- `Milestone 1/docs/data_dictionary.md`
- `Milestone 1/docs/dataset_validation_mapping.csv`
- `Milestone 2/docs/kpi_definitions.md`
- `Milestone 2/docs/methodology.md`

## Source Note

The supplied project documentation identifies the source datasets primarily by their dataset names and Kaggle origin. Exact external URLs should be added only when confirmed from the project's dataset validation mapping or source records.

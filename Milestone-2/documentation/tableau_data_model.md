# Tableau Data Model

## Hospital Performance Intelligence System

---

## 1. Purpose

This document describes the data model used for connecting the processed hospital datasets to Tableau.

The model is designed to support hospital operational analysis, patient flow analysis, department performance analysis and resource utilization analysis.

---

## 2. Processed Datasets

The following processed datasets are used in the project:

1. `hospital_overview_dataset.csv`
2. `patient_flow_dataset.csv`
3. `department_analytics_dataset.csv`
4. `resource_utilization_dataset.csv`

---

## 3. Dataset Grains

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per hospital admission |
| Patient Flow | One row per patient movement event |
| Department Analytics | One hospital, department and day |
| Resource Utilization | One hospital, department, day and resource type |

---

## 4. Hospital Overview Dataset

### Purpose

The Hospital Overview dataset provides admission-level information for overall hospital performance analysis.

### Important Fields

- `admission_id`
- `admission_date`
- `discharge_date`
- `admission_type`
- `admission_status`
- `patient_id`
- `department_id`
- `department_name`
- `ward_id`
- `bed_id`
- `length_of_stay_days`
- `gender`
- `disease_name`
- `total_amount`
- `insurance_covered_amount`
- `patient_payable_amount`
- `payment_status`

### Main Uses

- Total Admissions
- Average Length of Stay
- Occupancy Rate
- Admission trends
- Patient demographics
- Billing and payment analysis

---

## 5. Patient Flow Dataset

### Purpose

The Patient Flow dataset represents patient movement events during hospital visits.

### Important Fields

- `admission_id`
- `patient_id`
- `event_type`
- `event_date`
- `department_id`
- `department_name`
- `ward_id`
- `bed_id`
- `admission_type`
- `admission_status`
- `length_of_stay_days`

### Main Uses

- Admission and discharge trends
- Patient movement analysis
- Department-wise patient flow
- Daily patient activity
- Peak admission and discharge periods

---

## 6. Department Analytics Dataset

### Purpose

The Department Analytics dataset supports department-level performance comparison.

### Important Fields

- `department_id`
- `department_name`
- `department_type`
- `analysis_date`
- `total_admissions`
- `average_length_of_stay`
- `total_patient_days`
- `total_beds`
- `admissions_per_bed`
- `department_efficiency_score`

### Main Uses

- Department performance comparison
- Department efficiency score
- Admissions by department
- Average length of stay by department
- Department capacity analysis

---

## 7. Resource Utilization Dataset

### Purpose

The Resource Utilization dataset supports analysis of hospital beds and other available resources.

### Important Fields

- `department_id`
- `department_name`
- `analysis_date`
- `resource_type`
- `total_beds`
- `used_beds`
- `available_beds`
- `bed_utilization_rate`
- `total_patient_days`
- `occupancy_rate`

### Main Uses

- Bed utilization analysis
- Department capacity analysis
- Resource availability
- Occupancy comparison
- Resource planning

---

## 8. Tableau Relationships

The datasets can be connected using common fields.

| Dataset 1 | Dataset 2 | Relationship Field |
|---|---|---|
| Hospital Overview | Patient Flow | `admission_id` |
| Hospital Overview | Department Analytics | `department_id` |
| Department Analytics | Resource Utilization | `department_id`, `analysis_date` |

The relationship type should be selected carefully in Tableau to avoid duplicate records and incorrect aggregation.

---

## 9. Recommended Tableau Model

The recommended Tableau model uses the Hospital Overview dataset as the primary admission-level dataset.

The other datasets are connected according to their analytical grain.

```text
Hospital Overview
       |
       | admission_id
       |
Patient Flow

Hospital Overview
       |
       | department_id
       |
Department Analytics
       |
       | department_id + analysis_date
       |
Resource Utilization
```

---

## 10. KPI Data Sources

| KPI | Primary Dataset |
|---|---|
| Total Admissions | Hospital Overview |
| Average Length of Stay | Hospital Overview |
| Occupancy Rate | Hospital Overview and Resource Utilization |
| Readmission Rate | Not available |
| Bed Utilization Rate | Resource Utilization |
| Department Efficiency Score | Department Analytics |

---

## 11. Tableau Filters

The following filters are recommended for the dashboard:

- Admission Date
- Discharge Date
- Department Name
- Department Type
- Ward Name
- Admission Type
- Admission Status
- Gender
- Disease Category
- Payment Status

---

## 12. Data Quality Considerations

- Admission IDs must remain unique in the Hospital Overview dataset.
- Patient Flow may contain multiple events for one admission.
- Department Analytics must be analyzed at department and date level.
- Resource Utilization must be analyzed at department, date and resource level.
- Measures should not be duplicated through incorrect joins.
- Readmission Rate should be displayed as unavailable until a suitable dataset is integrated.

---

## 13. Conclusion

The Tableau data model provides a structured foundation for developing interactive dashboards.

The model separates admission-level, event-level, department-level and resource-level analysis. This helps maintain correct aggregation and supports reliable hospital performance reporting.
# KPI Definitions and Validation Document

## Hospital Performance Intelligence System

---

## 1. Purpose

This document defines the formulas, data sources, assumptions and validation status of the key performance indicators used in the Hospital Performance Intelligence System.

The KPIs are calculated using the processed analytical datasets created from the cleaned Core HMIS dataset.

---

## 2. KPI Summary

| KPI | Value | Unit | Status |
|---|---:|---|---|
| Total Admissions | 45,000 | Admissions | Validated |
| Average Length of Stay | 5.16 | Days | Validated |
| Occupancy Rate | 25.36 | Percentage | Validated using available capacity |
| Readmission Rate | Not available | Percentage | Dataset limitation |
| Bed Utilization Rate | 34.94 | Percentage | Preliminary |
| Department Efficiency Score | 90.13 | Score out of 100 | Preliminary |

---

## 3. Total Admissions

### Definition

Total Admissions represents the number of unique hospital admission records.

### Formula

```text
Total Admissions = COUNT DISTINCT(admission_id)
```

### Data Source

`hospital_overview_dataset.csv`

### Calculation

The KPI is calculated by counting distinct values of `admission_id`.

### Validation

- Total records checked: 45,000
- Unique admission IDs: 45,000
- Duplicate admission IDs: 0
- Validation status: Validated

---

## 4. Average Length of Stay

### Definition

Average Length of Stay represents the average number of days patients stay in the hospital.

### Formula

```text
Average Length of Stay = SUM(length_of_stay_days) / COUNT(admission_id)
```

### Data Source

`hospital_overview_dataset.csv`

### Calculation

The average is calculated using the `length_of_stay_days` field for all admission records.

### Validation

- Minimum length of stay: 1 day
- Maximum length of stay: 15 days
- Average length of stay: 5.16 days
- Invalid or negative values: 0
- Validation status: Validated

---

## 5. Occupancy Rate

### Definition

Occupancy Rate represents the percentage of available hospital bed capacity occupied during the observation period.

### Formula

```text
Occupancy Rate =
Total Patient-Days /
(Total Available Beds × Number of Days Covered) × 100
```

### Data Sources

- `hospital_overview_dataset.csv`
- `ward_cleaned.csv`
- `bed_cleaned.csv`

### Calculation

- Total patient-days: 231,975
- Total available beds: 415
- Number of days covered: 2,204

```text
Occupancy Rate =
231,975 / (415 × 2,204) × 100
= 25.36%
```

### Assumptions

- All registered beds are treated as available beds.
- The observation period is based on the minimum admission date and maximum discharge date.
- The calculation uses total patient-days rather than daily occupied-bed snapshots.

### Validation Status

Validated using available hospital capacity.

---

## 6. Readmission Rate

### Definition

Readmission Rate represents the percentage of patients who are admitted to the hospital again within a defined period after discharge.

### Formula

```text
Readmission Rate =
Number of Readmitted Patients /
Total Discharged Patients × 100
```

### Data Source

A dedicated patient readmission dataset is required for this KPI.

### Current Status

Not available in the current Core HMIS dataset.

### Reason

The available admission records do not provide a reliable, validated readmission indicator or sufficient information to confirm whether a patient was readmitted within a defined time window.

### Assumption

Readmission Rate will not be estimated using unsupported assumptions.

### Validation Status

Dataset limitation.

---

## 7. Bed Utilization Rate

### Definition

Bed Utilization Rate represents the percentage of registered beds that were used during the observation period.

### Formula

```text
Bed Utilization Rate =
Number of Used Beds /
Total Registered Beds × 100
```

### Data Sources

- `hospital_overview_dataset.csv`
- `bed_cleaned.csv`

### Calculation

- Total registered beds: 415
- Number of used beds: 145

```text
Bed Utilization Rate =
145 / 415 × 100
= 34.94%
```

### Assumptions

- A bed is considered used if it is associated with at least one admission record.
- The calculation measures the proportion of beds used at least once.
- This is different from daily bed occupancy.

### Validation Status

Preliminary.

---

## 8. Department Efficiency Score

### Definition

Department Efficiency Score is a composite score used to compare department-level operational performance.

### Formula

```text
Department Efficiency Score =
60% × Normalized Admissions per Bed
+
40% × Inverse Normalized Average Length of Stay
```

### Data Source

`department_analytics_dataset.csv`

### Calculation Method

1. Calculate total admissions for each department.
2. Calculate the average length of stay for each department.
3. Calculate admissions per bed.
4. Normalize department values to a 0–100 scale.
5. Calculate inverse normalized length of stay.
6. Combine both components using the selected weights.

```text
Efficiency Score =
(0.60 × Admissions Efficiency Component)
+
(0.40 × Length of Stay Efficiency Component)
```

### Assumptions

- Higher admissions per bed indicates better operational throughput.
- Lower average length of stay is treated as more efficient.
- The score is intended for comparative analysis and not as a clinical quality measure.
- The weighting scheme is a project-defined analytical assumption.

### Validation Status

Preliminary.

---

## 9. KPI Validation Summary

| Validation Check | Result |
|---|---|
| Duplicate admission IDs | 0 |
| Invalid length-of-stay values | 0 |
| Missing required KPI fields | 0 |
| Total admissions validation | Passed |
| Average length-of-stay validation | Passed |
| Occupancy rate validation | Passed using available capacity |
| Readmission rate validation | Not possible with current dataset |
| Bed utilization validation | Preliminary |
| Department efficiency validation | Preliminary |

---

## 10. Limitations

- The current implementation is primarily based on the Core HMIS dataset.
- Readmission Rate cannot be calculated reliably without a dedicated readmission dataset.
- Bed Utilization Rate measures beds used at least once, not daily utilization.
- Occupancy Rate is calculated using available bed capacity and patient-days.
- Department Efficiency Score is a preliminary comparative score based on project-defined weights.
- Additional approved datasets may improve patient outcome, resource and discharge-related analysis.

---

## 11. Conclusion

The implemented KPIs provide a validated starting point for hospital operational and patient-care analytics. The current results establish a baseline for admissions, length of stay, occupancy, bed usage and department performance.

Further validation and enhancement will be performed after integrating the remaining approved datasets, particularly for readmission and discharge-related analysis.
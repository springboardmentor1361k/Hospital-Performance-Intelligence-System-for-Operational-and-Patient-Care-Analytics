# Data Profiling Report

## Scope and Source

This profile covers the four local project CSVs in `data/raw/` and their prepared counterparts in `data/processed/`. The README describes the data as collected/generated for the project; no external source URL, API, or generation procedure is recorded. Counts and types below were measured from the files during this audit. Types are pandas `read_csv` inference on the processed CSVs; date columns are serialized as text and were separately parsed for validity.

## Dataset Summary

| Dataset | Raw rows | Processed rows | Columns | Exact duplicate rows removed | Processed duplicate rows | Processed missing cells | Missing cells (%) | Key/grain check |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Hospital Overview | 465 | 460 | 24 | 5 | 0 | 30 | 0.2717 | `admission_id` unique and non-null |
| Patient Flow | 1,134 | 1,126 | 20 | 8 | 0 | 1,390 | 6.1723 | `movement_id` unique; 0 unmatched admission IDs and 0 unmatched patient IDs |
| Department Analytics | 2,160 | 2,154 | 24 | 6 | 0 | 1,370 | 2.6501 | (`hospital_id`, `department_id`, `date`) unique |
| Resource Utilization | 6,472 | 6,462 | 24 | 10 | 0 | 10,953 | 7.0624 | `resource_utilization_id` and (`hospital_id`, `department_id`, `date`, `resource_type`) unique |

Missing-cell percentages use `missing cells / (processed rows * columns) * 100`. “Duplicate rows removed” compares exact full-row duplicates in raw input; processed duplicate counts are exact full-row duplicates. These measurements do not establish that every missing value is acceptable.

## Types and Columns

Processed CSV type counts from pandas inference:

| Dataset | `object` | `int64` | `float64` |
|---|---:|---:|---:|
| Hospital Overview | 20 | 1 | 3 |
| Patient Flow | 15 | 4 | 1 |
| Department Analytics | 6 | 9 | 9 |
| Resource Utilization | 12 | 4 | 8 |

See [the data dictionary](../docs/data_dictionary.md) for every field, its inferred type, identifying/foreign-key role, and a field-level description.

## Grain and Identifier Checks

- Hospital Overview: one row per admission; all 460 `admission_id` values are present and unique.
- Patient Flow: one row per movement event; all 1,126 `movement_id` values are present and unique. Repeated admission and patient IDs are expected at event grain.
- Department Analytics: one row per hospital, department, and date; no duplicate grain keys were found.
- Resource Utilization: one row per hospital, department, date, and resource type; no duplicate grain keys were found.
- Admission, patient, hospital, department, movement, and resource IDs matched the observed uppercase project formats; no tested pattern violations were found.
- All patient-flow admission and patient references matched Hospital Overview IDs.

## Dates and Categories

All non-missing values in the date fields parsed successfully during the audit. Observed date coverage is 2020-01-05 through 2025-12-22 for the daily department/resource data; Hospital Overview admission dates run from 2020-01-05 through 2025-12-16, and discharge dates through 2025-12-22. Patient-flow movement timestamps run from 2020-01-05 15:30 through 2025-12-22 04:45. `last_maintenance_date` has 2,154 non-missing values; all parsed values were valid.

Admission type values are `Elective`, `Emergency`, and `Urgent`; gender values are `Female`, `Male`, and `Other`. Department labels are not fully standardized by identifier: Hospital Overview has multiple names for `D001`, Patient Flow for `D009`, and Department Analytics for `D008`. For example, the processed department dataset contains both `Gen. Surgery` and `General Surgery` for `D008`. This is an unresolved quality observation, not a passed standardization check.

## Missingness and Quality Observations

- Hospital Overview: 7 missing `insurance_type` values and 23 missing `patient_satisfaction_score` values.
- Patient Flow: 460 missing `from_department_id`, `from_department_name`, and `bed_id` values, plus 10 missing `duration_in_department_hours` values. Missing origin fields coincide with initial admission events in the sample; no missing-value policy is documented.
- Department Analytics: 1,370 missing `avg_satisfaction_score` values.
- Resource Utilization: 2,154 missing each for `nurses_on_duty_snapshot` and `doctors_on_duty_snapshot`, 97 missing `avg_response_time_minutes`, 2,240 missing `resource_condition`, and 4,308 missing `last_maintenance_date` values.
- No processed file contains exact duplicate rows. Tested age, length-of-stay, billing, occupancy-rate, and utilization-rate bounds had zero violations.
- The cleaning notebook removes exact duplicates, trims text, standardizes selected ID/admission/gender values, parses selected dates, and checks numeric bounds and two patient-flow relationships. It does not document imputation, a completeness threshold, a full foreign-key audit, or a canonical department-name mapping.

## Limitations

This report describes observable file contents and checks, not provenance or clinical validity. Acceptable missingness thresholds, source-system definitions, and the Department Efficiency Score's component formula are not available in the repository. The score field is present in Department Analytics, but its component weights cannot be established from the available evidence.

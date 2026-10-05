# Data Dictionary

Types are inferred by pandas when reading the processed CSV files. Date/time columns remain `object` (text) in the CSV serialization; their non-missing values were parsed separately during profiling. Descriptions are based on field names and repository evidence. A business definition not established by the project is identified as unavailable.

## Hospital Overview

- **Purpose:** Admission-level hospital and patient record.
- **Grain:** One row per hospital admission.
- **Identifying field:** `admission_id` (unique and non-null in processed data).
- **Foreign keys:** `patient_id`, `hospital_id`, and `department_id`; patient and admission relationships are also referenced by Patient Flow.

| Field | Type | Description / business meaning |
|---|---|---|
| `admission_id` | object | Unique project identifier for an admission. |
| `patient_id` | object | Project identifier for the patient associated with the admission; may recur across admissions. |
| `hospital_id` | object | Project identifier for the hospital. |
| `hospital_name` | object | Hospital name associated with the record. |
| `department_id` | object | Project identifier for the admission department. |
| `department_name` | object | Department label; labels are not fully canonical by ID in the processed data. |
| `admission_date` | object | Admission date, stored as text in CSV. |
| `discharge_date` | object | Discharge date, stored as text in CSV. |
| `admission_type` | object | Admission category; observed values are Elective, Emergency, and Urgent. |
| `admission_source` | object | Recorded source of the admission. |
| `bed_id` | object | Bed identifier recorded for the admission. |
| `bed_type` | object | Recorded bed category. |
| `patient_age` | int64 | Patient age as recorded in the dataset. |
| `patient_gender` | object | Recorded gender category; observed values include Female, Male, and Other. |
| `diagnosis` | object | Recorded diagnosis text. |
| `insurance_type` | object | Recorded insurance/payment coverage category; some values are missing. |
| `total_bill_amount` | float64 | Admission-level bill amount as recorded; currency is not specified in the repository. |
| `payment_status` | object | Recorded payment status. |
| `discharge_status` | object | Recorded discharge outcome/status. |
| `patient_satisfaction_score` | float64 | Admission-level patient satisfaction score; scale definition is not documented. |
| `mortality_flag` | object | Recorded mortality indicator. |
| `readmission_flag` | object | Recorded readmission indicator; the KPI script counts rows equal to `Yes`. |
| `length_of_stay_days` | float64 | Length-of-stay value in days for the admission. |
| `admission_date_raw_text` | object | Additional admission-date text field retained in the dataset; its lineage is not documented. |

## Patient Flow

- **Purpose:** Patient movement events associated with admissions.
- **Grain:** One row per patient movement event.
- **Identifying field:** `movement_id` (unique and non-null in processed data).
- **Foreign keys:** `admission_id`, `patient_id`, `hospital_id`, `from_department_id`, and `current_department_id` where populated.

| Field | Type | Description / business meaning |
|---|---|---|
| `movement_id` | object | Unique project identifier for a movement event. |
| `admission_id` | object | Admission associated with the event; validated against Hospital Overview. |
| `patient_id` | object | Patient associated with the event; validated against Hospital Overview. |
| `hospital_id` | object | Hospital associated with the event. |
| `movement_sequence` | int64 | Recorded sequence number for the movement event. |
| `movement_type` | object | Event category; observed categories include Admission, Discharge, Department Change, Transfer, and ICU Transfer. |
| `from_department_id` | object | Origin department identifier; may be absent when no origin is recorded. |
| `current_department_id` | object | Department identifier associated with the event. |
| `from_department_name` | object | Origin department label; may be absent when no origin is recorded. |
| `current_department_name` | object | Current department label; some labels vary for the same department ID. |
| `bed_id` | object | Bed identifier associated with the event; may be missing. |
| `movement_datetime` | object | Movement timestamp, stored as text in CSV. |
| `movement_date` | object | Movement date, stored as text in CSV. |
| `duration_in_department_hours` | float64 | Recorded duration associated with the department event, in hours. |
| `year` | int64 | Year value stored for the movement. |
| `month` | int64 | Month value stored for the movement. |
| `day_of_week` | object | Day-of-week label stored for the movement. |
| `hour_of_day` | int64 | Hour value stored for the movement. |
| `shift` | object | Shift label stored for the movement; category definitions are not documented. |
| `is_peak_hour` | object | Stored peak-hour indicator; values are not documented as a formal coding standard. |

## Department Analytics

- **Purpose:** Daily operational and performance measures by hospital and department.
- **Grain:** One row per hospital + department + day.
- **Identifying fields:** The composite (`hospital_id`, `department_id`, `date`) is unique in processed data; there is no separate row ID.
- **Foreign keys:** `hospital_id` and `department_id`.

| Field | Type | Description / business meaning |
|---|---|---|
| `date` | object | Department observation date, stored as text in CSV. |
| `hospital_id` | object | Project identifier for the hospital. |
| `hospital_name` | object | Hospital name associated with the observation. |
| `department_id` | object | Project identifier for the department. |
| `department_name` | object | Department label; D008 has more than one label in the processed data. |
| `department_type` | object | Recorded department category. |
| `total_beds` | int64 | Recorded department bed capacity. |
| `occupied_beds_count` | int64 | Recorded occupied-bed count. |
| `bed_occupancy_rate_pct` | float64 | Stored bed-occupancy percentage; the row-level business definition is not documented. |
| `patients_admitted_count` | int64 | Recorded number of patients admitted for the observation. |
| `patients_discharged_count` | int64 | Recorded number of patients discharged for the observation. |
| `readmission_count` | int64 | Recorded readmission count. |
| `readmission_rate_pct` | float64 | Stored readmission percentage; denominator definition is not documented. |
| `mortality_count` | int64 | Recorded mortality count. |
| `mortality_rate_pct` | float64 | Stored mortality percentage; denominator definition is not documented. |
| `avg_length_of_stay_days` | float64 | Stored average length of stay in days; aggregation details are not documented. |
| `avg_treatment_time_hours` | float64 | Stored average treatment time in hours. |
| `transfer_events_count` | int64 | Recorded transfer-event count. |
| `nurses_on_duty` | int64 | Recorded number of nurses on duty. |
| `doctors_on_duty` | int64 | Recorded number of doctors on duty. |
| `staff_to_patient_ratio` | float64 | Stored staff-to-patient ratio; precise numerator/denominator convention is not documented. |
| `equipment_downtime_hours` | float64 | Recorded equipment downtime in hours. |
| `avg_satisfaction_score` | float64 | Stored average satisfaction score; scale definition is not documented and values are often missing. |
| `department_efficiency_score` | float64 | Existing department score (observed range 27.6-82.9); component methodology and weights are unavailable in the repository. |

## Resource Utilization

- **Purpose:** Resource availability, use, capacity, and maintenance observations.
- **Grain:** One row per hospital + department + date + resource type.
- **Identifying field:** `resource_utilization_id` is unique in processed data; the composite grain is also unique.
- **Foreign keys:** `hospital_id` and `department_id`.

| Field | Type | Description / business meaning |
|---|---|---|
| `resource_utilization_id` | object | Unique project identifier for the resource-utilization record. |
| `date` | object | Resource observation date, stored as text in CSV. |
| `hospital_id` | object | Project identifier for the hospital. |
| `hospital_name` | object | Hospital name associated with the observation. |
| `department_id` | object | Project identifier for the department. |
| `department_name` | object | Department label associated with the observation. |
| `resource_type` | object | Resource category; observed values are Bed, Equipment, and Clinical Staff. |
| `resource_category` | object | More specific recorded resource category. |
| `total_units_available` | int64 | Recorded number of available resource units. |
| `units_in_use` | int64 | Recorded number of resource units in use. |
| `units_under_maintenance` | int64 | Recorded number of units under maintenance. |
| `utilization_rate_pct` | float64 | Stored utilization percentage; row-level denominator definition is not documented. |
| `shortage_flag` | object | Recorded resource-shortage indicator. |
| `capacity_hours` | int64 | Recorded resource capacity in hours. |
| `utilized_hours` | float64 | Recorded utilized hours. |
| `idle_hours` | float64 | Recorded idle hours. |
| `downtime_hours` | float64 | Recorded downtime in hours. |
| `nurses_on_duty_snapshot` | float64 | Recorded nurse staffing snapshot; missing for some resource rows. |
| `doctors_on_duty_snapshot` | float64 | Recorded doctor staffing snapshot; missing for some resource rows. |
| `overtime_hours` | float64 | Recorded overtime in hours. |
| `avg_response_time_minutes` | float64 | Recorded average response time in minutes. |
| `resource_condition` | object | Recorded resource-condition label. |
| `maintenance_due_flag` | object | Recorded maintenance-due indicator. |
| `last_maintenance_date` | object | Last-maintenance date, stored as text in CSV; may be absent. |

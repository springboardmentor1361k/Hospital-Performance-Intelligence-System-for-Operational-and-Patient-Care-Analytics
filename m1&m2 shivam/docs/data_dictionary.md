# MedTrack_DV — Data Dictionary

This document describes every source dataset and every field in the four final analytical tables
(`data/processed/*.csv`) that support the Tableau dashboards. Produced by
`notebooks/03_data_normalization.ipynb`, verified by `notebooks/04_data_validation.ipynb`.

**Legend used throughout:**
🟢 direct from source · 🔵 derived/computed from source(s) · 🟡 bridged from Beds Management ·
🟠 benchmark from Readmission dataset · ⚪ not available (documented gap)

---

## 1. Source Datasets

### 1.1 HMIS — Hospital HMIS Dataset for Healthcare Analytics (PRIMARY / BACKBONE)

A relational schema of 19 tables (patient, admission, department, ward, bed, doctor, employee,
disease, billing, prescriptions, insurance, etc.) simulating **one hospital**, with real
primary/foreign-key relationships. Verified during profiling and cleaning: zero orphaned foreign
keys, zero duplicate primary keys, zero bad admission/discharge date ordering across all 19 tables.
Numeric sequential IDs. Every row of all four final tables originates here — it is the only
dataset with true admission-level detail.

**Known source-data issue:** 1,007 patients (4.3%) have at least one admission dated before their
recorded `date_of_birth`, producing an impossible negative age for 1,630 admissions. Flagged and
nulled in `hospital_overview_dataset.patient_age`, not silently fixed or dropped.

### 1.2 Beds Management (SUPPLEMENT)

4 flat files (`patients.csv`, `staff.csv`, `services_weekly.csv`, `staff_schedule.csv`) describing
a **different simulated hospital's** weekly staffing and bed demand. No shared key with HMIS —
`patient_id`/`staff_id` use their own hex namespace (`PAT-xxxx`, `STF-xxxx`), confirmed zero
overlap with HMIS's numeric IDs. `staff_id` also has **zero overlap between Beds Management's own
two files** (`staff.csv` vs `staff_schedule.csv`) — the real, working key between them is
`staff_name`. Aggregated at the week level (52 weeks + month, no year, no day — a calendar bridge
assuming year 2025 was built and verified against the data's own `month` column, 0 mismatches).
Covers only 4 of HMIS's 6 clinical departments (`emergency`, `surgery`, `general_medicine`→
Internal Medicine, `ICU`; `Pediatrics`/`Orthopedics` have no counterpart).

### 1.3 Readmission Dataset — Hospital Data for Patient Readmission Prediction (BENCHMARK ONLY)

1 flat file, 10,000 rows, another unrelated synthetic population. IDs renamed
`readm_patient_id`/`readm_doctor_id`/`readm_hospital_id` on load specifically so they can never be
mistaken for HMIS's own IDs. **Operational fields fail internal logic checks and are excluded
entirely**: `occupied_beds > hospital_beds_available` in 27.8% of rows, `checkout` before `checkin`
in 47.5% of rows, `patient_length_of_stay` matches the actual date gap in only 1.8% of rows,
`hospital_id` has 6,074 unique values despite a single constant `hospital_name`. Only
`discharge_status`, `readmission`, and `patient_disease` are trustworthy, used purely as a
disease-level statistical benchmark (7 of 19 HMIS diseases match by name after stripping
parenthetical abbreviations like "(COPD)"; the remaining 12 fall back to the dataset-wide average).

---

## 2. `hospital_overview_dataset.csv`

**Grain:** 1 row = 1 HMIS admission · **Row count:** 45,000 · **Primary key:** `admission_id`

| Field | Source | Description |
|---|---|---|
| admission_id | 🟢 HMIS | `admission.admission_id` |
| patient_id | 🟢 HMIS | `admission.patient_id` |
| hospital_id | 🔵 HMIS | hardcoded `1` — HMIS models only one hospital |
| hospital_name | 🔵 HMIS | hardcoded `"HMIS Hospital"` |
| department_id | 🟢 HMIS | `admission.department_id` |
| department_name | 🔵 HMIS | joined from `department.department_name` |
| admission_date | 🟢 HMIS | `admission.admission_date` |
| discharge_date | 🟢 HMIS | `admission.discharge_date` |
| admission_type | 🟢 HMIS | `admission.admission_type` |
| admission_source | ⚪ | no field for this in any of the 3 datasets |
| bed_id | 🟢 HMIS | `admission.bed_id` |
| bed_type | 🔵 HMIS | proxy via `bed.ward_id → ward.ward_type` |
| patient_age | 🔵 HMIS | `admission_date − patient.date_of_birth`; 1,630 rows nulled (impossible values, see §1.1) |
| patient_gender | 🟢 HMIS | `patient.gender` |
| diagnosis | 🔵 HMIS | joined from `disease.disease_name` via `admission.disease_id` |
| insurance_type | 🔵 HMIS | matched `patient_insurance` policy active on `admission_date`; ~24% match rate, rest NaN |
| total_bill_amount | 🔵 HMIS | joined from `billing.total_amount` |
| payment_status | 🔵 HMIS | joined from `billing.payment_status` |
| discharge_status | 🟢 HMIS | `admission.admission_status`, renamed — only ever `"Discharged"` in this data |
| patient_satisfaction_score | ⚪ | no survey/feedback table anywhere in HMIS |
| mortality_flag | ⚪ | no death/outcome field in HMIS; `admission_status` has only 1 unique value |
| readmission_flag | 🔵 HMIS | proxy: same patient re-admitted within 30 days of a prior discharge (not ground truth) |
| benchmark_mortality_rate | 🟠 Readmission | disease-level `% Deceased`, matched by normalized disease name |
| benchmark_readmission_rate | 🟠 Readmission | disease-level `mean(readmission)` |
| benchmark_satisfaction_score | 🟠 Readmission | disease-level `mean(patient_sat_score) / 16` (rescaled from a 1600-point scale) |
| benchmark_sample_size | 🟠 Readmission | row count the benchmark is based on |
| benchmark_match_type | 🟠 Readmission | `"disease-specific"` (7 diseases) or `"dataset-average fallback"` (12 diseases) |

---

## 3. `patient_flow_dataset.csv`

**Grain:** 1 row = 1 movement event · **Row count:** 90,000 (exactly 2 per admission) ·
**Primary key:** `movement_id`

> **Known limitation:** HMIS has no movement/transfer log at all. A real patient path
> (ED → Ward → ICU → Discharge) cannot be reconstructed from any of the 3 datasets. This table is
> limited to 2 synthetic events per admission — Admission and Discharge — using the same
> department/bed for both.

| Field | Source | Description |
|---|---|---|
| movement_id | 🔵 HMIS | generated sequential ID |
| admission_id | 🟢 HMIS | `admission.admission_id` |
| patient_id | 🟢 HMIS | `admission.patient_id` |
| hospital_id | 🔵 HMIS | hardcoded `1` |
| movement_sequence | 🔵 HMIS | `1` = Admission event, `2` = Discharge event |
| movement_type | 🔵 HMIS | `"Admission"` or `"Discharge"` only |
| from_department_id | ⚪ | no transfer log exists — always NaN |
| from_department_name | ⚪ | no transfer log exists — always NaN |
| current_department_id | 🟢 HMIS | `admission.department_id` |
| current_department_name | 🔵 HMIS | joined from `department.department_name` |
| bed_id | 🟢 HMIS | `admission.bed_id` |
| movement_datetime | 🟢 HMIS | `admission_date` or `discharge_date` |
| movement_date | 🔵 HMIS | date part of `movement_datetime` |
| duration_in_department_hours | 🔵 HMIS | full LOS in hours on the Admission row, `0` on Discharge |
| year, month, day_of_week | 🔵 HMIS | derived from `movement_datetime` |
| hour_of_day | 🔵 HMIS | derived; always `0` — HMIS dates carry no real time-of-day component |
| shift | 🔵 HMIS | binned from `hour_of_day` (Night/Morning/Evening) |
| is_peak_hour | 🔵 HMIS | `hour_of_day` between 9 and 17 |

---

## 4. `department_analytics_dataset.csv`

**Grain:** 1 row = 1 department + 1 day, scoped to the **6 clinical departments** (the 5
Admin/Diagnostic departments have no wards/beds and never receive admissions) ·
**Row count:** 13,224 · **Primary key:** `(department_id, date)`

| Field | Source | Description |
|---|---|---|
| date | 🔵 HMIS | generated calendar range spanning min/max admission and discharge dates |
| hospital_id, hospital_name | 🔵 HMIS | hardcoded |
| department_id, department_name, department_type | 🟢 HMIS | `department` table |
| total_beds | 🔵 HMIS | summed from `ward.total_beds` per department |
| occupied_beds_count | 🔵 HMIS | event-delta + cumulative-sum over admission/discharge dates |
| bed_occupancy_rate_pct | 🔵 HMIS | `occupied_beds_count / total_beds × 100` |
| patients_admitted_count | 🔵 HMIS | daily admission count per department |
| patients_discharged_count | 🔵 HMIS | daily discharge count per department |
| readmission_count, readmission_rate_pct | 🔵 HMIS | Table 2's `readmission_flag`, aggregated by department + discharge date |
| mortality_count, mortality_rate_pct | ⚪ | no mortality outcome field anywhere in HMIS |
| avg_length_of_stay_days | 🔵 HMIS | mean LOS of patients discharged that department+day |
| avg_treatment_time_hours | ⚪ | no treatment-time concept in any of the 3 datasets |
| transfer_events_count | ⚪ | no movement log exists (same limitation as Table 3) |
| nurses_on_duty, doctors_on_duty | 🟡 Beds Management | `staff_schedule.csv` (`present=1`), bridged via department+week → daily; only for the 4 mapped departments |
| staff_to_patient_ratio | 🔵 derived | `(nurses + doctors) / patients_admitted_count`, only where staffing data matched |
| equipment_downtime_hours | ⚪ | no equipment table exists in any of the 3 datasets |
| avg_satisfaction_score | 🟡 Beds Management | `services_weekly.patient_satisfaction`, same department+week bridge |
| department_efficiency_score | ⚪ in this table | computed separately, department-grain, in `department_efficiency_scores.csv` (see §6) |
| external_benchmark_available_beds | 🟡 Beds Management | `services_weekly.available_beds` — kept separate, never blended into `total_beds` (different simulated hospital) |
| external_benchmark_patients_refused | 🟡 Beds Management | `services_weekly.patients_refused` — same reasoning |

---

## 5. `resource_utilization_dataset.csv`

**Grain:** 1 row = 1 department + 1 day + 1 resource type · **Row count:** 13,224 ·
**Primary key:** `resource_utilization_id`

> **Known limitation:** only `resource_type = 'Bed'` rows exist. No Equipment rows are possible
> (no equipment table in any of the 3 datasets). A dated Clinical Staff resource row is not yet
> built in this version, though `beds_staff.csv` + `beds_staff_schedule.csv` could support one for
> the 4 mapped departments — see the project's methodology notes for this as a proposed next step.

| Field | Source | Description |
|---|---|---|
| resource_utilization_id | 🔵 HMIS | generated sequential ID |
| date, hospital_id, hospital_name, department_id, department_name | 🔵 HMIS | same as Table 3 |
| resource_type | 🔵 HMIS | hardcoded `"Bed"` |
| resource_category | ⚪ | not yet built — could be filled from `ward.ward_type` (pure HMIS, no external bridge needed) |
| total_units_available | 🔵 HMIS | = Table 3's `total_beds` |
| units_in_use | 🔵 HMIS | = Table 3's `occupied_beds_count` |
| units_under_maintenance | ⚪ | no such concept for beds in HMIS |
| utilization_rate_pct | 🔵 HMIS | = Table 3's `bed_occupancy_rate_pct` |
| shortage_flag | 🔵 HMIS | `utilization_rate_pct > 90%` (assumed threshold) |
| capacity_hours, utilized_hours, idle_hours | 🔵 HMIS | `total_units_available/units_in_use × 24` and the difference — approximations, not true occupied-hours |
| downtime_hours | ⚪ | no maintenance/downtime data for beds in HMIS |
| external_benchmark_available_beds, external_benchmark_patients_refused | 🟡 Beds Management | same bridge as Table 3 |

---

## 6. Supporting Output Files

| File | Grain | Purpose |
|---|---|---|
| `disease_outcome_benchmarks.csv` | 1 row per HMIS disease (19/20 rows) | Disease-level mortality/readmission/satisfaction benchmark from the Readmission dataset, feeding Table 2's `benchmark_*` columns |
| `validation_report.csv` | 1 row per check | Output of `04_data_validation.ipynb` — PK uniqueness, grain sanity, value-range validity, cross-table consistency, completeness scoring |
| `kpi_summary.csv` | 1 row per KPI (6 rows) | The 6 mandatory KPIs — see `kpi_definitions.md` |
| `department_efficiency_scores.csv` | 1 row per department (6 rows) | KPI 6 breakdown — connect to `department_analytics_dataset` via a Tableau relationship on `department_id`, not a flat merge (avoids repeating one department-level number ~2,200 times) |

---

## 7. Fields That Remain Genuinely Unfillable

These are not cleaning failures or a sign the wrong datasets were chosen — no field like these
exists in **any** of the 3 approved datasets:

- `admission_source`, real per-admission `mortality_flag` (Hospital Overview)
- `from_department_id`/`from_department_name`, `transfer_events_count` (no movement/transfer log exists anywhere)
- `equipment_downtime_hours`, `units_under_maintenance`, any Equipment resource row (no equipment table exists anywhere)

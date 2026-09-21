# MedTrack_DV — Data Dictionary

Documents every column in the four final analytical tables built from the HMIS dataset:
`hospital_overview_dataset.csv`, `patient_flow_dataset.csv`, `department_analytics_dataset.csv`,
`resource_utilization_dataset.csv`. For each table: grain, row count, column-by-column source/derivation,
and fields that were evaluated but are genuinely not available in this dataset.

Single-hospital note: HMIS has no `hospital_id`/`hospital_name` column anywhere in the source data.
A placeholder `hospital_id = 1`, `hospital_name = "HMIS Hospital"` is applied uniformly across all
four tables so Tableau/BI tooling has a consistent field to key off, even though there is only one hospital.

---

## 1. `hospital_overview_dataset.csv`
**Grain:** one row per admission. **Rows:** 45,000.

| Column | Source / Derivation |
|---|---|
| hospital_id, hospital_name | Placeholder constant (see note above) |
| admission_id | admission.admission_id (primary key) |
| patient_id | admission.patient_id |
| department_id, department_name, department_type | admission.department_id → department |
| ward_id, ward_name, ward_type | admission.ward_id → ward |
| bed_id, bed_number | admission.bed_id → bed |
| admission_date, discharge_date | admission |
| length_of_stay_days | discharge_date − admission_date |
| admission_type | admission.admission_type (Elective / Emergency) |
| patient_age_at_admission | admission_date − patient.date_of_birth |
| patient_gender, blood_group, city | patient |
| disease_name, disease_category | admission.disease_id → disease |
| primary_doctor_id / name / specialization | **Proxy.** Doctor who ordered the *earliest* diagnostic test for that admission (via patient_diagnostic → doctor → employee). Resolves for **70.0%** of admissions; remainder = "No diagnostic record." HMIS has no literal "attending physician" field on `admission`. |
| diagnostic_test_count | count(patient_diagnostic) per admission |
| prescription_count, distinct_drug_count | count / nunique(prescription) per admission |
| total_bill_amount, insurance_covered_amount, patient_payable_amount | billing (joined via admission_id → bill_id) |
| payment_status, payment_mode | billing |
| insurance_provider_name, insurance_provider_type | **Proxy.** patient_insurance policy whose [policy_start_date, policy_end_date] window covers admission_date. Resolves for only **24.0%** of admissions (most patients have no policy active on that exact date); remainder = "No active policy on file." Note: this is a *provider-attribution* rate — `billing.payment_mode = "Insurance"` (80% of bills) is the reliable signal for whether insurance was *used*, separate from which provider. |
| readmission_flag | **Derived proxy, not clinically verified.** 1 if admission_date falls within 30 days of the same patient's previous discharge_date, else 0. 1,120 of 45,000 admissions (2.49%) flagged. |
| readmission_gap_days | Days between this admission and the same patient's prior discharge; null for a patient's first admission (51.7% of rows — expected, not a defect). |
| year, quarter, month, month_name, day_of_week | Derived from admission_date |

**Evaluated but not available:** discharge_status / disposition, mortality_flag, patient_satisfaction_score, admission_source (referral / walk-in / transfer). None of these exist anywhere in HMIS.

---

## 2. `patient_flow_dataset.csv`
**Grain:** one row per flow event. HMIS has no literal patient-transfer/movement log, so every admission
contributes an **Admission** event and a **Discharge** event, and every diagnostic test contributes a
**Diagnostic Test** event (a genuine, date-validated move to Radiology/Pathology — confirmed 100% of
test_date values fall inside their admission's stay). **Rows:** 153,269 (45,000 + 45,000 + 63,269).

| Column | Source / Derivation |
|---|---|
| flow_event_id | Derived surrogate key (primary key) |
| event_type | 'Admission' / 'Discharge' / 'Diagnostic Test' |
| event_date | admission_date / discharge_date / test_date respectively |
| admission_id, patient_id | admission / patient_diagnostic |
| department_id, department_name | Home department for Admission/Discharge rows; the **test's own department** (Radiology/Pathology) for Diagnostic Test rows — this is what makes cross-department movement visible |
| ward_id, ward_name, ward_type, bed_id | Populated only on Admission/Discharge rows — null by design on Diagnostic Test rows (a test isn't tied to a ward) |
| admission_type, disease_name, disease_category, patient_gender, patient_age_at_admission | Carried from the parent admission |
| length_of_stay_days | Populated only on Discharge rows |
| doctor_id / name / specialization | Populated only on Diagnostic Test rows (the test-ordering doctor) |
| test_name, test_category, result_status | Populated only on Diagnostic Test rows |
| year, quarter, month, month_name, day_of_week | Derived from event_date |

**Evaluated but not available:** hour_of_day, shift, is_peak_hour (admission/discharge/test dates carry no time component — date only), true ward-to-ward transfer sequence, duration_in_department_hours, movement_sequence within a single stay.

---

## 3. `department_analytics_dataset.csv`
**Grain:** one row per department per calendar day. Built as a full daily calendar spine
(2020-01-01 → latest discharge date) × all 11 departments, so trend lines have no gaps.
**Rows:** 24,244.

| Column | Source / Derivation |
|---|---|
| hospital_id, hospital_name, date, year, quarter, month, month_name, day_of_week | Calendar spine |
| department_id, department_name, department_type | department |
| total_beds | sum(ward.total_beds) for wards in this department. **Static capacity**, not day-specific. The 5 non-clinical departments (Radiology, Pathology, Pharmacy, Billing, HR) correctly show 0 — they have no wards. |
| admissions_count | count(admissions where admission_date = date & department) |
| discharges_count | count(admissions where discharge_date = date & department) |
| estimated_census | **Modeled estimate, not measured.** Running cumulative sum of (admissions_count − discharges_count) per department, clipped at 0. HMIS's `bed.csv` is only ever a current snapshot (270 occupied / 145 available at time of extraction), so there is no real historical daily census to use instead. |
| bed_occupancy_rate_pct | estimated_census / total_beds × 100 |
| readmission_count | Count of readmission_flag = 1 admissions that date/department |
| readmission_rate_pct | readmission_count / admissions_count × 100 (daily grain — noisy; recommend rolling up to monthly for stable KPI reporting, see kpi_definitions.md) |
| avg_length_of_stay_days | Mean length_of_stay_days of that day's discharges, per department |
| total_bill_amount, avg_bill_amount | billing summed/averaged via admission → department → date |
| diagnostic_test_count | count(patient_diagnostic) that date, joined via diagnostic_test.department_id — the field that brings Radiology/Pathology meaningfully into this table despite having zero admissions |
| doctor_headcount, nurse_headcount | **Static proxy.** count(employee.role = 'Doctor'/'Nurse') where employee.department_id = this department. Constant across every date — not a true daily on-duty count (no such data exists in HMIS). |
| staff_to_patient_ratio | (doctor_headcount + nurse_headcount) / estimated_census |
| department_efficiency_score | See formula in kpi_definitions.md. **Null 45–51% of days** by design (needs both admission and discharge activity that day) — never average this raw column directly; roll up components first. |

**Evaluated but not available:** mortality_count/rate, equipment_downtime_hours, avg_satisfaction_score, transfer_events_count, true daily doctors/nurses on duty (only a static headcount proxy is possible).

---

## 4. `resource_utilization_dataset.csv`
**Grain:** department + date + resource_type — but only the **Bed** block is genuinely daily.
Built as three honest blocks rather than pretending all three are equally time-series data.
**Rows:** 13,549 (13,224 Bed + 75 Staff + 250 Drug Inventory).

**Block A — Bed** (daily, 6 clinical departments only)
| Column | Source |
|---|---|
| date, department_id/name | Calendar spine |
| total_units_available | ward.total_beds |
| units_in_use | estimated_census (same modeled derivation as table 3) |
| utilization_rate_pct | units_in_use / total_units_available × 100 |

**Block B — Staff** (static snapshot — **no date axis**, one row per ward/shift)
| Column | Source |
|---|---|
| ward_id, ward_name, department_id/name, shift | staff_assignment.ward_id → ward → department |
| units_in_use | count(staff_assignment) by ward + shift |
| doctor_count, nurse_count, technician_count, pharmacist_count, admin_count | employee.role, pivoted by ward + shift. Note: staff_assignment.csv in this dataset only ever carries **Nurse** and **Technician** roles — doctors are not ward-assigned, so doctor_count is 0 throughout Block B (doctor staffing is only available via the department-level headcount proxy in table 3). |

**Block C — Drug Inventory** (snapshot as of last_restock_date; **assumption**: assigned to the Pharmacy department, since individual drugs aren't tied to a specific clinical department in HMIS)
| Column | Source |
|---|---|
| drug_id, drug_name, drug_category | drug |
| units_in_use, reorder_level_threshold | drug_inventory (current_stock, reorder_level, renamed) |
| shortage_flag | derived: units_in_use < reorder_level_threshold (44 of 250 drugs flagged) |
| manufacturer_name, reliability_rating | drug_manufacturer |

**Important caveat — checked and confirmed not predictive:** `reliability_rating` shows essentially zero correlation with either stock level (r = 0.047) or shortage_flag (r = −0.044). Shortage rate is nearly identical across reliability bands (17.4% vs 17.7%). Do not build charts or narratives implying reliability drives shortages in this dataset — it doesn't.

**Also note:** `drug_name` is **not unique** — only 142 distinct names across 250 drugs (e.g., "Nostrum" appears on 6 different drug_ids). Always key/group by `drug_id`, never by `drug_name` alone, or values from unrelated drugs will be silently combined.

**Evaluated but not available:** equipment (no equipment table exists in HMIS at all), true daily staff on-duty counts, overtime_hours, avg_response_time_minutes, maintenance_due_flag/downtime.

---

## Fields present but confirmed non-actionable (checked, not assumed)

| Field | Table | Finding |
|---|---|---|
| `city` | hospital_overview | 14,868 distinct values across 45,000 admissions; top city = 0.13% of admissions. Faker-generated placeholder names (e.g., "North Thomasside," "Espinozaberg") — not real, geocodable places. **Do not build a map from this field** — Tableau's geocoding will not resolve it and any result would be misleading, not just incomplete. |
| `blood_group` | hospital_overview | Distribution is near-uniform across all 8 types (12.0%–13.1% each, including within individual departments) — does not reproduce real-world population skew. Still legitimate for blood-bank stock planning based on *this hospital's own* patient mix, but should not be presented as matching general clinical statistics. |
| `reliability_rating` | resource_utilization (Drug Inventory) | See Block C note above — not correlated with shortage risk in this dataset. |

---

## Rejected external datasets (not merged into any table)

- **Healthcare_Data_Analysis_for_readmission.csv** — no genuine shared key with HMIS (patient_id/doctor_id overlaps were coincidental or zero), plus internal integrity failures (27.8% of rows show occupied_beds > available_beds; inconsistent date formats). Excluded entirely.
- **Hospital Beds Management** (beds_patients, beds_services_weekly, beds_staff, beds_staff_schedule) — weekly data has no year anchor (cannot be mapped to HMIS's 2020–2025 real calendar); covers only 4 of HMIS's 6 clinical departments; staff/patient IDs belong to a different, unrelated population. Excluded entirely.

Full rejection rationale is documented in `dataset_sources.md`.
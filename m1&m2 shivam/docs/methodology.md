# MedTrack_DV — Methodology

## 1. Project approach

MedTrack_DV was built from a single approved source: the **Hospital HMIS Dataset for Healthcare
Analytics** — a relational synthetic hospital-management dataset (19 linked tables: admission,
patient, department, ward, bed, doctor, employee, disease, billing, drug inventory, etc.) covering
one hospital's operations from 2020-01-01 through 2025-12-31.

Two other candidate datasets were evaluated and formally rejected before any merging was attempted
(see `dataset_sources.md` for full rationale): a readmission-focused CSV with no genuine shared key
to HMIS, and a "Hospital Beds Management" dataset with no year anchor on its weekly data and only
partial department coverage. The project proceeds on HMIS alone, with known gaps documented rather
than filled with unreliable external data.

Pipeline order followed: **Data Collection → Data Cleaning → Data Standardization → Dataset
Validation → ETL (four-table build) → KPI Engineering → Tableau Data Model → Dashboard Development →
Dashboard Integration → Documentation**, matching the mentor-specified workflow.

## 2. Why four tables, and why these grains

The mentor guidance was explicit that the four analytical tables should not simply be four unrelated
flat exports of the same admission data — each one is built at the grain that actually matches its
dashboard's purpose:

| Table | Grain | Reason |
|---|---|---|
| `hospital_overview_dataset` | 1 row = 1 admission | Matches HMIS's natural transactional entity |
| `patient_flow_dataset` | 1 row = 1 flow event | HMIS has no literal movement/transfer log, so this table is a constructed event log (Admission, Discharge, Diagnostic Test) rather than a direct export — the closest honest substitute for true patient-movement data |
| `department_analytics_dataset` | 1 row = 1 department + 1 day | A full calendar spine × all 11 departments, so trend charts have no gaps, and so departments with zero admissions (Radiology, Pathology, Pharmacy, Billing, HR) are still representable via their own activity (diagnostic tests, staffing) |
| `resource_utilization_dataset` | 1 row = department + date + resource_type | Deliberately built as three separate blocks (Bed / Staff / Drug Inventory) rather than one uniform grain, because only Bed data is genuinely daily — Staff and Drug Inventory are current snapshots in the source data with no date history at all |

Before any merging, referential integrity was checked and confirmed 100% consistent: ward.department_id
always matches admission.department_id; bed.ward_id always matches admission.ward_id; every
diagnostic_test.department_id resolves to Radiology or Pathology; every test_date falls inside its
admission's stay window.

## 3. Proxy and estimated fields — what they are and how confident to be in them

HMIS does not contain every field the project doc's KPI list implies, and rather than force an
unrelated dataset to fill the gap (explicitly against project guidance), several fields were built as
clearly-labeled derived proxies:

- **`primary_doctor` (hospital_overview_dataset):** HMIS has no "attending physician" field on
  `admission`. The proxy uses the doctor who ordered the *earliest* diagnostic test for that
  admission. Resolves for 70.0% of admissions; the remaining 30% have no diagnostic record and are
  labeled accordingly, not guessed.
- **`insurance_provider` (hospital_overview_dataset):** matched via policy date-range containment
  (`policy_start_date` ≤ `admission_date` ≤ `policy_end_date`). Resolves for only 24.0% of
  admissions — most patients don't have a policy active on that exact date in the source data. This
  is a provider-*attribution* rate, distinct from `billing.payment_mode = "Insurance"` (80% of bills),
  which is the reliable signal for whether insurance was actually used to pay.
- **`readmission_flag`:** a documented 30-day same-patient proxy, not a clinically verified
  readmission. See `kpi_definitions.md` for the eligibility-adjusted denominator logic used when
  turning this into a rate.
- **`estimated_census` / bed occupancy (department_analytics_dataset, resource_utilization_dataset):**
  HMIS's `bed.csv` is only ever a current point-in-time snapshot (270 occupied / 145 available at
  extraction time) — there is no real historical daily bed-occupancy record anywhere in the source
  data. `estimated_census` is a modeled estimate: a per-department running cumulative sum of
  (admissions − discharges), clipped at zero. This is explicitly labeled "estimated" everywhere it
  appears on the dashboards and in KPI reporting, and was sanity-checked against implausible runaway
  values (max single-day modeled occupancy observed: 58%, within plausible bounds).
- **`doctor_headcount` / `nurse_headcount` (department_analytics_dataset):** a static proxy —
  `employee.department_id` headcount, constant across every date. Not a true daily on-duty count,
  since no such time-varying staffing record exists in HMIS. `resource_utilization_dataset`'s Staff
  block is similarly a snapshot with no date axis at all (`staff_assignment.csv` has no date column).

## 4. Fields checked and found not to carry a real signal

Two fields exist in the source data but were verified, not assumed, to be non-informative for
analytical use:

- **`city` (patient location):** 14,868 distinct values across 45,000 admissions; the single most
  common city accounts for only 0.13% of admissions. Values follow a Faker-library placeholder
  pattern (direction/prefix + first name + invented suffix, e.g. "North Thomasside") rather than real
  place names, so they are not geocodable and show no real catchment clustering. No map or
  city-ranking chart was built from this field for this reason.
- **`reliability_rating` (drug manufacturer):** correlation with stock level = 0.047, with
  shortage_flag = −0.044 — both statistically meaningless. Shortage rate is nearly identical across
  reliability bands (17.4% vs 17.7%). No chart implying reliability predicts shortage risk was built
  from this field.
- **`blood_group`:** distribution is near-uniform across all 8 types (12.0%–13.1% each, including
  within individual departments), unlike real-world population statistics. Retained for blood-bank
  stock-planning purposes (a hospital cares about its own patients' actual mix regardless of whether
  it matches textbook averages), but explicitly not presented as reflecting general clinical
  population data.

## 5. Data quality issue documented, not corrected

Validation surfaced a genuine data-quality defect in the source relationship between `patient.csv`
and `admission.csv`: **1,630 admissions (3.6%)** have an `admission_date` that falls *before* the
patient's recorded `date_of_birth` — i.e., the patient had not yet been born according to the source
data at the time of that admission. Ages for these rows range from −1 to −6. This was confirmed to be
a genuine impossible value (not a calculation error — traced and reproduced independently), and is
left as a documented limitation rather than silently corrected, per the "do not automatically delete
every outlier" guidance in the project brief. Any age-based KPI or chart should be read with this in
mind; these rows were not excluded from the four tables.

## 6. Tableau data model

Given the relationship pitfalls of mixing tables at genuinely different grains, the two data-source
groupings were built deliberately: `hospital_overview_dataset` ↔ `patient_flow_dataset` (related on
`admission_id`, a true 1-to-many), and `department_analytics_dataset` ↔ `resource_utilization_dataset`
(related on the compound key `department_id` + `date`). Extracts (.hyper) were used throughout rather
than live connections, both for performance (150K+ rows in patient_flow_dataset, six years of daily
data in department_analytics_dataset) and because Tableau Public requires extracts.

Two workbook-level parameters (`Department Selector`, `Year Selector`) were used in place of native
per-data-source quick filters, specifically because the two data source groupings otherwise fail to
sync filters against each other, and because `department_analytics_dataset` legitimately contains 11
departments (including 5 non-admitting ones) while `hospital_overview_dataset` only ever contains 6 —
a parameter with a manually-defined, deliberately scoped value list avoids both problems at once.

## 7. Known overall limitations

- No mortality data, discharge disposition, or patient satisfaction score exists anywhere in HMIS.
- No equipment inventory or downtime data exists in HMIS at all.
- No true daily/historical staffing record exists — only a current snapshot.
- Single-hospital dataset; no multi-facility comparison is possible.
- `estimated_census` and everything derived from it (occupancy, bed utilization, staffing ratios) is
  a modeled estimate, not a measured historical value.
- `readmission_flag` is a 30-day same-patient proxy, not a clinically confirmed readmission.
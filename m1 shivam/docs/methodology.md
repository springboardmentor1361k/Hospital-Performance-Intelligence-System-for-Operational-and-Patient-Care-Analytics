# MedTrack_DV — Methodology

## 1. Project Objective

Build a Hospital Operations & Patient Analytics Dashboard covering patient admissions/discharges,
patient flow, department performance, resource utilization, and the 6 mandatory KPIs, as four
interconnected Tableau dashboards backed by a validated, documented data pipeline.

## 2. Architecture

```
RAW DATA
   |
DATA PROFILING           (01_data_loading.ipynb)
   |
DATA CLEANING            (02_data_cleaning.ipynb)
   |
DATA NORMALIZATION       (03_data_normalization.ipynb)
   |
   ├── HMIS builds all 4 final tables independently
   ├── Beds Management bridged in (department + week dimensions)
   └── Readmission dataset bridged in (disease dimension)
   |
DATA VALIDATION           (04_data_validation.ipynb)
   |
KPI ENGINEERING            (05_kpi_engineering.ipynb / generate_hospital_kpis.py)
   |
TABLEAU DATA MODEL  →  DASHBOARD DEVELOPMENT  →  TESTING  →  SUBMISSION
```

Each stage's notebook is independently re-runnable and does not assume in-memory state from a
previous notebook — every notebook reloads its inputs fresh from `data/processed/`.

## 3. Dataset Selection

Three datasets were used, not the four originally scoped:

| Dataset | Role | Included? |
|---|---|---|
| HMIS | Core/backbone | ✅ |
| Beds Management | Resource/staffing supplement | ✅ |
| Readmission Prediction | Outcome benchmark | ✅ |
| Inpatient Discharges (SPARCS) | Additional inpatient volume | ❌ — evaluated and excluded |

**Why the 4th dataset was excluded:** it only offered one genuinely new field (`admission_source`)
as a benchmark, not a real value; it could not address any of the project's actual structural gaps
(no movement log, no equipment table, no dated staff schedule); it faces the same no-shared-key
limitation as the other two supplements; and at ~832MB the effort-to-value ratio did not justify
inclusion. This is a documented decision, not an oversight.

## 4. Core Methodological Principle: Bridging, Not Merging

None of the three datasets share a real join key. HMIS uses its own numeric IDs; Beds Management
uses an unrelated hex ID space (`PAT-xxxx`, `STF-xxxx`); the Readmission dataset uses yet another
unrelated population entirely. **No patient-level or admission-level join was ever attempted
between datasets.** Instead:

- **HMIS builds all four final tables on its own first.** It is internally consistent (verified:
  0 orphaned foreign keys, 0 duplicate primary keys, 0 bad date ordering across all 19 tables) and
  is the only source with true admission-level detail.
- **Beds Management is bridged in via two constructed dimensions**, not a row-level key:
  - *Department name bridge*: its 4 service categories mapped to 4 of HMIS's 6 clinical
    departments (`Pediatrics`, `Orthopedics` have no counterpart and are left NaN, not guessed).
  - *Time bridge*: its week-number + month fields (no year, no day) were converted to real
    calendar dates, assuming year 2025 (consistent with `beds_patients.csv`'s own real dates), with
    each week given a **variable length** so weeks partition each month exactly — verified 0
    month-alignment mismatches and 0 overlapping date ranges before any merge was trusted.
  - Merged only into the two tables that are already aggregated (Department Analytics, Resource
    Utilization) via `LEFT JOIN`, HMIS remaining authoritative — never into the admission-grain
    tables (Hospital Overview, Patient Flow), since no honest attribution to a specific admission
    exists.
- **The Readmission dataset is bridged in via disease name only.** Its operational fields (dates,
  bed counts, hospital/doctor IDs) were tested and found internally inconsistent (see §6) and are
  excluded entirely. Only `discharge_status`, `readmission`, and `patient_disease` are used, as a
  **benchmark**, not ground truth: 7 of 19 HMIS diseases match by name after normalization
  (stripping parenthetical abbreviations like "(COPD)"); the remaining 12 fall back to the
  dataset-wide average, with every row explicitly labeled `benchmark_match_type` so the difference
  is never hidden.

## 5. Grain Preservation

Per the four required grains (1 admission / 1 movement event / 1 department+day / 1
department+day+resource type), every construction step was followed by an explicit assertion, not
a visual spot-check:

```python
assert hospital_overview_dataset['admission_id'].is_unique
assert len(patient_flow_dataset) == len(admission) * 2
assert department_analytics_dataset.duplicated(subset=['department_id','date']).sum() == 0
```

Every bridge merge is preceded by a row-count snapshot and followed by an assertion that the count
is unchanged, preventing the classic "1 admission × 5 movements × 3 resources = 15 rows" fan-out
the project doc warns against.

## 6. Data Quality Findings and Handling Decisions

| Finding | Decision |
|---|---|
| 1,007 HMIS patients (4.3%) have an admission dated before their recorded `date_of_birth` | Flagged and nulled the resulting impossible `patient_age` (1,630 admissions) — the admission row itself is kept, only the invalid derived value is removed |
| Readmission dataset: `occupied_beds > hospital_beds_available` in 27.8% of rows; checkout before checkin in 47.5%; `patient_length_of_stay` matches actual date gap in only 1.8% | All operational fields from this dataset excluded from any calculation — flagged via `dates_reliable`/`bed_counts_reliable`/`length_of_stay_reliable` columns during cleaning, never silently fixed |
| Beds Management: `staff_id` has 0% overlap between `staff.csv` and `staff_schedule.csv` | Discovered by actually running the foreign-key check, not assumed. The real working key is `staff_name` (100% of `staff.csv`'s 110 names found in `staff_schedule.csv`) |
| A first version of the week→date bridge produced 104/208 mismatches against the data's own `month` column | Rebuilt to read `month` directly from the data (ground truth) rather than predicting it, and to give each week a variable length instead of a fixed 7 days — the fixed-7-day version had caused a silent row-count duplication bug, caught by an `assert len(df) == before_rows` check |

## 7. Readmission Rate: Proxy vs. Benchmark, Explicitly Distinguished

Two different signals exist in the pipeline and are never conflated:

- **`readmission_flag`** (Hospital Overview, used for KPI 4): a same-patient, 30-day proxy
  computed entirely from HMIS's own admission history. This is what the KPI reports.
- **`benchmark_readmission_rate`** (Hospital Overview, supplementary): the Readmission dataset's
  real, disease-level readmission rate, usable for comparison but not as the KPI itself, since it
  describes a different, unrelated patient population.

## 8. Known, Documented Structural Gaps

No amount of additional joining resolves these — none of the three approved datasets contain the
underlying concept at all:

- Real per-admission `mortality_flag` and `admission_source` (Hospital Overview)
- `from_department_id`/`from_department_name`, `transfer_events_count` — **no dataset among the
  three contains a patient movement/transfer log**, so Patient Flow is limited to 2 synthetic
  events (Admission, Discharge) per admission rather than a real intra-stay path
- `equipment_downtime_hours`, any Equipment `resource_type` row — no equipment table exists in any
  of the three datasets

These are stated plainly in `data_dictionary.md` §7 and are not treated as failures — a dashboard
tile simply isn't built for a metric with no underlying data, which is normal, not broken.

## 9. KPI Methodology Highlights

- **Occupancy Rate / Bed Utilization Rate** are capacity-weighted (`sum/sum`), not a simple mean
  of daily percentages, to avoid a 6-bed department counting equally to a 90-bed department.
- **Readmission Rate** uses the 30-day proxy defined in §7, with the denominator being *all*
  admissions (a patient's first-ever admission scores 0, it is not excluded).
- **Department Efficiency Score** is a documented composite (30% occupancy-fit + 30% LOS-rank +
  25% readmission + 15% satisfaction), computed only from components available for each department
  and automatically re-weighted when one is missing (Pediatrics/Orthopedics have no satisfaction
  data, so their score is computed from the remaining 85% of weight, not penalized for the gap).
  Full derivation in `docs/kpi_definitions.md` §6.

## 10. Tableau Data Model Guidance

Because the four final tables have different grains, they should be connected in Tableau via
**relationships** (not a single flattened join, and not blends), on `department_id` where
applicable. `department_efficiency_scores.csv` (department-grain, 6 rows) should also be connected
via relationship rather than merged into `department_analytics_dataset.csv` (department+day grain,
13,224 rows) — a flat merge would repeat each department's single efficiency score roughly 2,200
times, which the project doc explicitly warns against.
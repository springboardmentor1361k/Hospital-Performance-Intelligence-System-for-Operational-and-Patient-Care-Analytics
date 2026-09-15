# MedTrack_DV — KPI Definitions

The project requires 6 mandatory KPIs. Every formula and source field below is implemented in
`notebooks/05_kpi_engineering.ipynb` and `scripts/generate_hospital_kpis.py` (the two are
kept in sync — the script is the re-runnable CLI version of the notebook), and produces
`data/processed/kpi_summary.csv` and `data/processed/department_efficiency_scores.csv`.

**Verified results (current data):**

| KPI | Value |
|---|---|
| Total Admissions | 45,000 |
| Occupancy Rate | 30.28% |
| Average Length of Stay | 5.16 days |
| Readmission Rate | 2.19% |
| Bed Utilization Rate | 30.28% |
| Department Efficiency Score | 51.97 – 81.95 (per department, see §6) |

---

## 1. Total Admissions

**Definition:** The total number of distinct hospital admissions in the dataset.

**Formula:**
```
COUNTD(admission_id)
```

**Source:** `hospital_overview_dataset.admission_id`

**Calculation note:** Counted from Hospital Overview only — never from Patient Flow, which has
exactly 2 rows per admission and would silently double the count.

---

## 2. Occupancy Rate

**Definition:** The share of total bed capacity that is occupied, across all departments and days.

**Formula:**
```
sum(occupied_beds_count) / sum(total_beds) x 100
```

**Source:** `department_analytics_dataset.occupied_beds_count`, `department_analytics_dataset.total_beds`

**Calculation note:** This is a **capacity-weighted average**, not a simple mean of each day's
percentage. A simple mean would treat a 6-bed department and a 90-bed department as equally
important; weighting by actual bed count avoids that distortion.

---

## 3. Average Length of Stay (LOS)

**Definition:** The average number of days between admission and discharge, per admission.

**Formula:**
```
mean(discharge_date - admission_date)
```

**Source:** `hospital_overview_dataset.admission_date`, `hospital_overview_dataset.discharge_date`

**Calculation note:** Computed at admission-level (Hospital Overview), as the project doc
specifies, rather than re-derived from Department Analytics' daily aggregates.

---

## 4. Readmission Rate

**Definition:** The share of admissions that represent a readmission of the same patient.

**Formula:**
```
count(readmission_flag = 1) / count(all admissions) x 100
```

**Source:** `hospital_overview_dataset.readmission_flag`

**Definition of `readmission_flag`:** `1` if the same `patient_id` has a prior discharge within
**30 days** before this admission's start date; `0` otherwise (including every patient's first
admission).

**⚠️ Known limitation — read before citing this number:** This is a **documented proxy**, built
entirely from HMIS's own admission history. It is **not** the Readmission dataset's real
`readmission` flag, because no patient-level link exists between HMIS and that dataset (different,
unrelated synthetic populations — see `data_dictionary.md` §1.3). The Readmission dataset's real
flag only contributes a **disease-level benchmark** (`benchmark_readmission_rate` in Hospital
Overview), which can be compared against this proxy but should not be confused with it.

**Eligible population:** every admission is eligible (denominator = all admissions); a patient's
first-ever admission simply scores 0, it is not excluded from the denominator.

---

## 5. Bed Utilization Rate

**Definition:** The share of available bed capacity currently in use.

**Formula:**
```
sum(units_in_use) / sum(total_units_available) x 100     [resource_type = 'Bed' only]
```

**Source:** `resource_utilization_dataset.units_in_use`, `resource_utilization_dataset.total_units_available`

**Calculation note:** Restricted to `resource_type == 'Bed'` — the only resource type any of the 3
datasets can support (no equipment table, no dated staff schedule exists for a general resource
calculation). **This value is numerically identical to Occupancy Rate (KPI 2)** in the current
data, because Resource Utilization's Bed rows were themselves derived from the same
`department_analytics_dataset` occupancy numbers. This is expected given the current data
sources, not a calculation error — if a Clinical Staff resource row is added in a future revision,
this KPI would need to be scoped explicitly to `resource_type == 'Bed'` to keep meaning "beds," not
"all resources."

---

## 6. Department Efficiency Score

**Definition:** A composite 0–100 score per department reflecting how efficiently it is operating,
combining occupancy, length of stay, readmissions, and (where available) patient satisfaction.

**Why a composite, and why these components:** The project doc requires a documented score built
from "relevant departmental indicators such as occupancy, LOS, readmission, downtime." Downtime and
mortality — two indicators a full implementation might include — are not available from any of the
3 approved datasets (see `data_dictionary.md` §7) and are excluded rather than estimated.

**Components** (each independently normalized to a 0–100 "higher is better" scale):

| Component | Weight | Formula | Rationale |
|---|---|---|---|
| Occupancy fit | 30% | `100 - |occupancy_pct - 80|`, floored at 0 | Efficiency peaks near 80% occupancy — too low wastes capacity, too high risks overcrowding |
| LOS efficiency | 30% | Relative rank across departments: shortest average LOS = 100, longest = 0 | A relative comparison across this hospital's own departments, not an absolute clinical judgment |
| Readmission | 25% | `100 - readmission_rate_pct` | Lower readmission rate = higher score |
| Satisfaction | 15% | `avg_satisfaction_score` directly | Only available for the 4 departments the Beds Management bridge matched (Emergency, Surgery, ICU, Internal Medicine) |

**Combination formula:**
```
department_efficiency_score = weighted average of available components,
                                re-weighted to sum to 100% when a component is missing
```

For example, Pediatrics and Orthopedics have no satisfaction data (Beds Management doesn't cover
them), so their score is `(occupancy×30 + los×30 + readmission×25) / 85`, not penalized for a
missing input.

**Source:** `department_analytics_dataset` (all components), aggregated per `department_id`.

**Output:** `department_efficiency_scores.csv` — 1 row per department (6 rows), **not** merged
into `department_analytics_dataset` (which is department+day grain) to avoid repeating one
department-level number ~2,200 times. Connect the two in Tableau via a relationship on
`department_id`.

**Interpretation of current results:** Five departments score 80.7–82.0. **ICU scores 51.97** —
driven almost entirely by an `los_score` of 0.00, meaning ICU has the longest average length of
stay relative to every other department. This is the formula correctly surfacing a real,
clinically-expected pattern (ICU stays are longer by nature), not a data or calculation error.

---

## Change Log / Known Next Steps

- `resource_category` (Resource Utilization) is not yet split by `ward.ward_type` — feasible from
  HMIS alone, would add real granularity (confirmed real variety exists per department).
- `avg_treatment_time_hours` (Department Analytics) is not yet populated — a proxy (admission →
  first diagnostic test) is feasible from HMIS alone, covering ~70% of admissions.
- A dated `Clinical Staff` resource row is not yet built — feasible via `beds_staff.csv` (roster
  capacity) + `beds_staff_schedule.csv` (daily present count) for the 4 mapped departments.
- Hospital Overview's `patient_satisfaction_score` could be strengthened using `beds_patients.csv`
  (currently unused, per-patient satisfaction data) alongside `services_weekly`'s weekly average.

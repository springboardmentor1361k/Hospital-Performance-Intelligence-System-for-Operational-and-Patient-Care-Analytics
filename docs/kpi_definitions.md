# KPI Definitions — MedTrack_DV

**Milestone 2, Module 3: Hospital KPI Engineering**

This document defines the 6 mandatory KPIs required by the project guidance document. Every KPI states its formula, source fields, denominator, and any documented limitation — per the mentor's instruction that formulas must be explicit and validated, not assumed.

Source datasets: `hospital_overview_dataset.csv`, `resource_utilization_dataset.csv`, `department_analytics_dataset.csv` (all in `data/processed/`), built from the HMIS core dataset (see `docs/methodology.md` for the full data model and dataset validation).

---

## 1. Total Admissions

**Formula:**
```
Total Admissions = COUNTD(admission_id)
```

**Source:** `hospital_overview_dataset.csv` — `admission_id` (one row = one admission, so a simple row count equals distinct admission count).

**Result:** 45,000

**Interpretation:** Total volume of hospital admissions in the dataset period. This is the base denominator for several other KPIs.

---

## 2. Occupancy Rate

**Formula:**
```
Occupancy Rate (%) = SUM(occupied_beds_count) / SUM(total_beds_capacity) x 100
```

**Source:** `resource_utilization_dataset.csv` — `occupied_beds_count` (derived by exploding each admission's `admission_date` → `discharge_date` range into daily active-bed records) and `total_beds_capacity` (from HMIS `ward.total_beds`, summed per department).

**Denominator:** Total available bed-capacity-days across the full dataset period, summed across all departments.

**Result:** 30.31%

**Interpretation:** Hospital-wide average fraction of bed capacity that was occupied, across the entire period. Reported at hospital level here; the same underlying occupied/capacity figures are also available broken down by department (see `Department_KPIs` sheet in `hospital_final_dataset.xlsx`).

---

## 3. Average Length of Stay (LOS)

**Formula:**
```
Average LOS (days) = MEAN(discharge_date - admission_date)
```

**Source:** `hospital_overview_dataset.csv` — `length_of_stay_days` (already derived in notebook `02_data_integration.ipynb`).

**Result:** 5.16 days

**Interpretation:** Average number of days a patient stays in hospital per admission, hospital-wide. Department-level LOS is also available (see Department_KPIs sheet) and varies significantly by clinical intensity — see the note on ICU under Department Efficiency Score below.

---

## 4. Readmission Rate

**Formula:**
```
Readmission Rate (%) = COUNT(is_readmission = True) / COUNT(all admissions) x 100
```

**Definition of "readmission":** An admission is flagged as a readmission if the same `patient_id` has a previous discharge within 30 days before this admission's `admission_date` (derived in notebook `02_data_integration.ipynb`, Section 6).

**Denominator:** All admissions in `hospital_overview_dataset.csv` (45,000) — not just patients with a prior admission. This is a conservative, hospital-wide readmission rate.

**Result:** 2.19% (986 readmissions out of 45,000 admissions)

**Documented limitation:** This KPI is derived entirely from HMIS `admission` data. It is **not** cross-matched with the separately-sourced "Hospital Data for Patient Readmission Prediction" Kaggle dataset, because that dataset's `patient_id` values are independently generated and do not correspond to HMIS `patient_id` values — merging them row-level would be a fabricated join, which the mentor's document explicitly prohibits ("do not force unrelated datasets together").

---

## 5. Bed Utilization Rate

**Formula:**
```
Bed Utilization Rate (%) = SUM(occupied_beds_count) / SUM(total_beds_capacity) x 100   [per department]
```

**Source:** `resource_utilization_dataset.csv`, grouped by `department_id`.

**Result (hospital-wide):** 30.31% — identical to Occupancy Rate at hospital level, because both use the same underlying occupied/capacity ratio (this matches the formulas given in the project guidance document, which defines both KPIs identically). **The distinction in this project is grain, not formula**: Occupancy Rate is reported hospital-wide (Hospital Overview dashboard); Bed Utilization Rate is reported per department (Department Analytics / Resource Utilization dashboards) — see per-department values in the table below.

**Per-department values:**

| Department        | Bed Utilization Rate (%) |
|--------------------|---------------------------|
| Pediatrics         | 31.16 |
| ICU                | 30.98 |
| Orthopedics        | 30.56 |
| Internal Medicine  | 30.41 |
| Emergency          | 30.28 |
| Surgery            | 29.00 |

---

## 6. Department Efficiency Score (composite, 0–100)

**Components:**
- `occupancy_score` = department Bed Utilization Rate (%), capped at 100
- `readmission_score` = 100 − department Readmission Rate (%), clipped to [0, 100]
- `los_score` = 100 × (2 − department_avg_LOS / hospital_avg_LOS), clipped to [0, 100]
  - A department whose average LOS equals the hospital-wide average scores 100 on this component.
  - A department with double the hospital-wide average LOS scores 0.

**Weights (documented, adjustable):**
- Occupancy: 40%
- Readmission: 30%
- LOS: 30%

**Formula:**
```
Department Efficiency Score =
    0.40 x occupancy_score
  + 0.30 x readmission_score
  + 0.30 x los_score
```

**Excluded components:** Staff-to-patient ratio and equipment downtime were considered per the project guidance document, but were **intentionally excluded** because the source data (`staff_assignment`, `bed`) has no daily/date field in HMIS — it is a static current-state snapshot, not a time series. Including them in a per-day efficiency score would require fabricating daily values that do not exist in the source data, which the mentor's document explicitly prohibits.

**Results:**

| Department         | Admissions | Avg LOS (days) | Readmission Rate (%) | Bed Utilization (%) | Efficiency Score |
|---------------------|-----------|----------------|------------------------|------------------------|-------------------|
| Pediatrics          | 8,438     | 4.69           | 2.20                   | 31.16                  | **71.80** |
| Orthopedics         | 5,924     | 4.68           | 1.94                   | 30.56                  | 71.64 |
| Internal Medicine   | 7,695     | 4.66           | 2.30                   | 30.41                  | 71.47 |
| Emergency           | 8,777     | 4.69           | 2.20                   | 30.28                  | 71.45 |
| Surgery             | 10,126    | 4.67           | 2.18                   | 29.00                  | 70.95 |
| ICU                 | 4,040     | 9.98           | 2.33                   | 30.98                  | **43.61** |

**Interpretation:**

ICU scores substantially lower (43.61) than every other department, almost entirely because of the `los_score` component: ICU's average LOS (9.98 days) is roughly double the hospital-wide average (5.16 days).

**This does not indicate genuine ICU inefficiency.** ICU patients are clinically expected to require longer stays than general wards due to the severity of conditions treated there. The scoring formula compares every department's LOS against a single hospital-wide benchmark, which is a simplification that does not account for differences in clinical intensity across departments.

**Recommended future improvement (not implemented in this iteration):** Benchmark each department's LOS against its own historical average or an external clinical LOS standard for that specialty, rather than the hospital-wide average, before combining it into the composite score. This limitation is documented here rather than silently adjusted, so dashboard viewers correctly interpret the ICU score as a modeling artifact rather than an operational problem.

---

## Summary Table

| # | KPI | Value | Source Sheet |
|---|-----|-------|----------------|
| 1 | Total Admissions | 45,000 | KPI_Summary |
| 2 | Occupancy Rate | 30.31% | KPI_Summary |
| 3 | Average Length of Stay | 5.16 days | KPI_Summary |
| 4 | Readmission Rate | 2.19% | KPI_Summary |
| 5 | Bed Utilization Rate | 30.31% (hospital) / per-dept in Department_KPIs | KPI_Summary / Department_KPIs |
| 6 | Department Efficiency Score | Range 43.61–71.80 across departments | Department_KPIs |

All KPIs are generated by `scripts/generate_hospital_kpis.py` and saved to `data/processed/hospital_final_dataset.xlsx`.



## Manual Validation (Excel cross-check)

All KPIs were independently verified in Excel against the Python/Pandas
calculations, per the project guidance document's testing requirement.

| KPI | Python Result | Excel Manual Check | Match |
|-----|---------------|---------------------|-------|
| Total Admissions | 45,000 | 45,000 | ✅ |
| Average LOS | 5.16 days | 5.16 days | ✅ |
| Readmission Rate | 2.19% | 2.19% | ✅ |
| Occupancy / Bed Utilization Rate | 30.31% | 30.31373% | ✅ |

All four cross-checked KPIs matched. Department Efficiency Score was
verified visually against its component formula in the
`Department_KPIs` sheet of `hospital_final_dataset.xlsx`.
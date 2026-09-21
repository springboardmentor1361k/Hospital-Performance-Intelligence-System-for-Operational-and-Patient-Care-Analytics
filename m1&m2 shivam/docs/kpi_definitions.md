# MedTrack_DV — KPI Definitions

The 6 mandatory KPIs required by the project doc, each with its formula, source table, grain(s) computed,
denominator/proxy decisions, and the actual cross-validation result produced by
`05_kpi_engineering.ipynb`. Numbers below are real output, not illustrative — reproduced and verified
before this document was written.

**Cross-cutting rules applied to every KPI:**
- Computed at three grains: hospital-wide overall, by department, and (where a date exists) by month.
- Never average a pre-computed daily rate to get a coarser-grain figure — the raw numerator/denominator
  are re-summed first, then divided once.
- Every proxy or estimate is labeled at the point of use, not buried in a separate file.
- Cross-validated against a second, independent calculation wherever the data allows it.

---

## 1. Total Admissions
**Formula:** `COUNTD(admission_id)`
**Source:** `hospital_overview_dataset`

| Grain | Result |
|---|---|
| Overall | **45,000** |
| Emergency | 8,777 |
| ICU | 4,040 |
| Internal Medicine | 7,695 |
| Orthopedics | 5,924 |
| Pediatrics | 8,438 |
| Surgery | 10,126 |

**Cross-check:** `COUNTD(admission_id)` in `hospital_overview_dataset` vs `SUM(admissions_count)` in `department_analytics_dataset` — **45,000 = 45,000, MATCH** (overall and by every department, 0 mismatches).

---

## 2. Occupancy Rate
**Formula:** `SUM(estimated_census) / SUM(total_beds) × 100`
**Source:** `department_analytics_dataset`, filtered to the 6 clinical departments only (the 5 non-clinical departments have `total_beds = 0` by definition and must not dilute this KPI).

**Modeled, not measured** — `estimated_census` is a derived proxy (see data_dictionary.md); label this everywhere it's shown.

| Grain | Result |
|---|---|
| Overall | **25.36%** |
| Emergency | 24.92% |
| ICU | 28.15% |
| Internal Medicine | 25.01% |
| Orthopedics | 25.15% |
| Pediatrics | 25.66% |
| Surgery | 23.86% |

**Reasonableness check:** max single-day occupancy observed across all departments = 58.0% — within plausible bounds (does not run away to implausible multiples of bed capacity, a known risk of an uncapped cumulative-sum estimate).

---

## 3. Average Length of Stay
**Formula:** `MEAN(discharge_date − admission_date)`
**Source:** `hospital_overview_dataset`

| Grain | Mean | Median |
|---|---|---|
| Overall | **5.16 days** | 4.0 days |
| Emergency | 4.69 | 4.0 |
| ICU | **9.98** | 10.0 |
| Internal Medicine | 4.66 | 4.0 |
| Orthopedics | 4.68 | 4.0 |
| Pediatrics | 4.69 | 4.0 |
| Surgery | 4.67 | 4.0 |

Both mean and median reported — protects against a few long stays quietly skewing the headline number. ICU's mean is more than double every other department's, driven by genuinely longer clinical stays (not a data error).

**Cross-check:** direct department-level mean (hospital_overview) vs a discharges-weighted reconstruction from `department_analytics_dataset`'s daily `avg_length_of_stay_days` — **exact match on all 6 departments, diff = 0.0 everywhere.**

---

## 4. Readmission Rate
**Formula:** 30-day same-patient proxy. **Documented, not clinically verified** — HMIS has no discharge-disposition or same-diagnosis linkage to confirm a true unplanned readmission.
**Source:** `hospital_overview_dataset`

**Denominator decision:** uses *eligible discharges*, not all admissions. A discharge is only "eligible" to show a subsequent readmission if at least 30 days remained in the observed data window after it — otherwise the case is right-censored and would unfairly count as "no readmission" just because the window ran out. Observed window ends 2026-01-12; eligibility cutoff = 2025-12-13. **476 discharges were excluded from the denominator** for this reason.

| Grain | Rate |
|---|---|
| Overall (eligibility-adjusted, **documented default**) | **2.52%** |
| Overall (naive: numerator / all admissions — reference only) | 2.49% |
| Emergency | 2.43% |
| ICU | **2.76%** |
| Internal Medicine | 2.58% |
| Orthopedics | 2.17% (lowest) |
| Pediatrics | 2.51% |
| Surgery | 2.65% |

**Cross-check:** readmission count (numerator only — eligibility adjustment affects the denominator, not the count) — `SUM(readmission_flag)` in hospital_overview vs `SUM(readmission_count)` in department_analytics — **1,120 = 1,120, MATCH.**

---

## 5. Bed Utilization Rate
**Formula:** `SUM(units_in_use) / SUM(total_units_available) × 100`
**Source:** `resource_utilization_dataset`, filtered to `resource_type = 'Bed'` first (the table also contains Staff and Drug Inventory rows where these same column names mean something different).

| Grain | Result |
|---|---|
| Overall | **25.36%** |
| Emergency | 24.92% |
| ICU | 28.15% |
| Internal Medicine | 25.01% |
| Orthopedics | 25.15% |
| Pediatrics | 25.66% |
| Surgery | 23.86% |

**Cross-check:** this is functionally the same underlying number as Occupancy Rate (KPI 2), reshaped through the long resource table — **25.36% = 25.36%, MATCH**, confirming the reshape introduced no distortion.

---

## 6. Department Efficiency Score
**Formula:** weighted composite, 0–100 scale:
`0.4 × Occupancy Score + 0.3 × LOS Score + 0.3 × Readmission Score`
- Occupancy Score = `MIN(100, Occupancy Rate)`
- LOS Score = `MAX(0, MIN(100, 100 − (Avg LOS / 15 × 100)))` — 15 days = the observed maximum LOS in this dataset, used as the "worst case" anchor
- Readmission Score = `MAX(0, MIN(100, 100 − Readmission Rate))`

**Source:** `department_analytics_dataset` — computed from **rolled-up components**, never by averaging the raw daily `department_efficiency_score` column (which is null 45–51% of days by design).

| Department | Occupancy % | Avg LOS | Readmission % | **Efficiency Score** |
|---|---|---|---|---|
| Pediatrics | 25.66 | 4.69 | 2.51 | **60.13** |
| Orthopedics | 25.15 | 4.68 | 2.17 | 60.05 |
| Internal Medicine | 25.01 | 4.66 | 2.58 | 59.92 |
| Emergency | 24.92 | 4.69 | 2.43 | 59.85 |
| Surgery | 23.86 | 4.67 | 2.65 | 59.40 |
| ICU | 28.15 | **9.98** | 2.76 | **50.47** (lowest) |

**Face-validity note (documented, not a defect):** ICU has the *highest* occupancy of any department but scores *lowest* on efficiency. This is not a scoring error — ICU's average LOS (9.98 days) is nearly double every other department's, and LOS carries 30% weight in the formula, which correctly drags its score down despite strong occupancy. Interpret ICU's score in the context of its structurally different patient population, not as a straight comparison against the other five departments.

---

## Summary — all cross-checks passing

| Check | Result |
|---|---|
| Total Admissions: hospital_overview vs department_analytics | 45,000 = 45,000 ✓ |
| Avg LOS: direct vs department_analytics-reweighted | exact match, all 6 departments ✓ |
| Readmission count: hospital_overview vs department_analytics | 1,120 = 1,120 ✓ |
| Bed Utilization Rate vs Occupancy Rate (same grain) | 25.36% = 25.36% ✓ |

Every KPI above was independently recomputed from a second source table where the data allowed it, per the project doc's explicit instruction not to claim a figure without actually calculating it.
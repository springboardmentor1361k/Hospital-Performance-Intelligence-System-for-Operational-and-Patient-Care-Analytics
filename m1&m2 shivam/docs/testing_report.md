# MedTrack_DV — Testing Report (Milestone 4)

**Project:** MedTrack_DV – Hospital Operations & Patient Analytics Dashboard
**Dataset:** HMIS only (19 linked tables, 2020-01-01 to 2025-12-31)
**Tested by:** <your name>  |  **Date:** <date>

Testing is split into three parts, as the project brief asks: **Data Testing**, **KPI Testing**, **Tableau (Dashboard) Testing**.

> **How to read the status column:** PASS = verified by running a check and seeing the result. FAIL (documented) = a real issue found and explained. RETEST = to be re-checked on the rebuilt dashboards.

---

## 1. Data Testing

Run through `04_validate_four_tables.ipynb` on the four processed tables.

### 1.1 Primary key uniqueness — 7 / 7 PASS
| Table | Key tested | Result |
|---|---|---|
| hospital_overview | admission_id | PASS (unique) |
| patient_flow | event_id | PASS (unique) |
| department_analytics | department_id + date | PASS (unique) |
| resource_utilization | department_id + date + resource_type | PASS (unique) |
| (other key checks) | see notebook output | PASS |

### 1.2 Grain checks — 5 / 5 PASS
| Table | Expected grain | Result |
|---|---|---|
| hospital_overview | 45,000 rows = 1 admission each | PASS |
| patient_flow | 45,000 Admission + 45,000 Discharge + 63,269 Diagnostic Test events | PASS |
| department_analytics | 2,204 days × 11 departments = 24,244 rows | PASS |
| resource_utilization (Bed block) | 2,204 days × 6 clinical departments = 13,224 rows | PASS |
| resource_utilization (Staff / Drug) | snapshot rows, no date history | PASS (by design) |

### 1.3 Range checks — 14 / 16 PASS, 2 FAIL (documented)
| Check | Result |
|---|---|
| Dates inside 2020-01-01 → 2025-12-31 (admission) | PASS |
| Length of stay ≥ 0 | PASS |
| Rates between 0 and 100 | PASS |
| Counts non-negative | PASS |
| **Age ≥ 0 — hospital_overview** | **FAIL: 1,630 admissions have negative age (−1 to −6)** |
| **Age ≥ 0 — patient_flow** | **FAIL: 5,576 event rows (same 1,630 admissions repeated per event)** |

**Explanation:** the source data has 1,630 admissions (3.6%) where `admission_date` is *before* the patient's `date_of_birth`. Confirmed as a source-data defect, not a calculation error.
**Decision:** documented, not deleted (the brief says not to automatically remove outliers). Age-based charts must carry a note.

### 1.4 Cross-table consistency — 6 / 6 PASS
| Check | Result |
|---|---|
| admission_id set in hospital_overview = admission_id set in patient_flow | PASS |
| Every department_id in department_analytics exists in the department master | PASS |
| SUM(admissions_count) = 45,000 = rows in hospital_overview | PASS |
| SUM(discharges_count) = 45,000 | PASS |
| SUM(readmission_flag) in hospital_overview = SUM(readmission_count) in department_analytics = 1,120 | PASS |
| Bed-block department IDs ⊆ department_analytics IDs | PASS |

### 1.5 Completeness — PASS
100% non-null on all core fields in all four tables. Columns that are *allowed* to be blank (documented): `primary_doctor` (30% blank, no diagnostic test), `insurance_provider` (76% blank, no active policy on admission date), daily `department_efficiency_score` (blank on days with no discharges).

### 1.6 Duplicates
Because every table has a unique key (1.1), full-row duplicates are logically impossible. No duplicate keys found.

> **Note:** a fresh re-run of the validation script was not possible in the last session (the working environment was reset). The numbers above come from the earlier verified run. **Before submitting, re-run notebook 04 and paste its console output into Appendix A.**

---

## 2. KPI Testing

Each KPI was computed in Python (`05_kpi_engineering.ipynb`) and compared against what the Tableau dashboard shows.

| KPI | Python result | Tableau result | Status |
|---|---|---|---|
| Total Admissions | 45,000 | 45,000 | PASS |
| Admissions by dept | Emergency 8,777 · ICU 4,040 · Int. Med 7,695 · Ortho 5,924 · Peds 8,438 · Surgery 10,126 | same | PASS |
| Occupancy Rate | 25.36% | 25.36% | PASS |
| Average LOS | 5.16 days (median 4.0) | 5.16 | PASS |
| LOS by dept | ICU 9.98, others 4.66–4.69 | same | PASS |
| Readmission Rate (overall) | 2.52% adjusted / **2.49% naive** | 2.49% | PASS (see note) |
| Readmission by dept | adjusted 2.43 / 2.76 / 2.58 / 2.17 / 2.51 / 2.65 | 2.40 / 2.72 / 2.56 / 2.14 / 2.49 / 2.62 | PASS (see note) |
| Bed Utilization | 25.36% | 39.69% on the first build (missing Resource Type = Bed filter) | **FAIL → fix → RETEST** |
| Efficiency Score | Peds 60.13 · Ortho 60.05 · Int. Med 59.92 · Emergency 59.85 · Surgery 59.40 · ICU 50.47 | computed from Tableau rollup | RETEST after rebuild |

**Readmission note (verified):** Python's default divides readmissions by *eligible* discharges (excludes 476 discharges in the last 30 days of the data). Tableau divides by *all* admissions. Recomputing the naive version from the raw data gives exactly Emergency 2.40, ICU 2.72, Internal Medicine 2.56, Orthopedics 2.14, Pediatrics 2.49, Surgery 2.62, overall 2.49 — identical to Tableau. So the difference is the denominator, not an error. Both are documented; the dashboard should label which one it shows.

**Internal cross-checks (all PASS):**
- Total admissions: hospital_overview = department_analytics = 45,000
- Avg LOS: direct vs department-reweighted, diff = 0.0 on all 6 departments
- Readmission count: 1,120 = 1,120
- Bed Utilization = Occupancy = 25.36% (same underlying number)

---

## 3. Tableau Testing

Observed on the first build of the four dashboards. Results marked RETEST must be re-checked on the rebuilt version.

### 3.1 Functional tests
| # | Test | Expected | Observed | Status |
|---|---|---|---|---|
| T1 | Department Selector on Dashboard 1 | All charts and KPIs update | Works | PASS |
| T2 | Year Selector on Dashboard 1 | All charts update | Total Admissions showed 7,694 for 2025; true value is 7,595 | **FAIL → RETEST** |
| T3 | Department Selector on Dashboards 2–4 | Charts update | Works | PASS |
| T4 | Filter sync between the two data sources | Same selection on all dashboards | Works via parameters | PASS |
| T5 | Navigation between dashboards | Each button opens the right dashboard | Present, labels need renaming | RETEST |
| T6 | Parameter action (click department → filter) | Required by brief | Not implemented | RETEST |

### 3.2 Visual / data tests
| # | Test | Observed | Status |
|---|---|---|---|
| V1 | Total Admissions (D1) vs Home→Diagnostic flow total (D2) | Different on purpose: D2 counts only admissions that reached a diagnostic test (about 70%) | PASS (explained) |
| V2 | Total admissions vs blood-group total (D1) | Match (45,000) | PASS |
| V3 | Department score table admissions vs D1 | Different when a Year filter is applied | RETEST |
| V4 | Trend charts at the right edge | Drop at the end: admissions stop on 2025-12-31 but discharges continue to 2026-01-12 (114 discharges in Jan 2026, 0 admissions) | PASS (explained); hide partial Jan 2026 |
| V5 | LOS by Department | Built as bubbles, not box plot | RETEST |
| V6 | Heatmaps | Flat colour, needs continuous scale | RETEST |
| V7 | Patient Volume legend | Discharge series missing | RETEST |
| V8 | Dashboard 4 title | Still reads "Department Analytics" | RETEST |
| V9 | Drug Shortage Watch | Ratios above 1 when summing over repeated drug names; now uses AVG and an exclusion filter, which can hide critical drugs | RETEST with unique "Drug Label" |
| V10 | Tableau Public publish | Extract error on `department_summary_corrected.csv` | RETEST |

### 3.3 Performance tests
| # | Test | Result |
|---|---|---|
| P1 | Dashboard load time on laptop | RETEST (record seconds) |
| P2 | Extract (.hyper) used instead of live connection | PASS |

### 3.4 Layout tests (record after rebuild)
Fixed size 1600 × 900 · Fonts consistent · No scrollbars · No blurry charts · Titles match nav labels.

---

## 4. Issues log and fixes
| ID | Issue | Cause | Fix | Status |
|---|---|---|---|---|
| I1 | Negative age | Source DOB after admission date | Documented, kept | Open (by design) |
| I2 | Year Selector count 7,694 vs 7,595 | Year field ambiguous across related tables (counts admissions with any 2025 event) | Use YEAR([Admission Date]) / YEAR([Event Date]) | Fix on rebuild |
| I3 | Bed Utilization 39.69% | Resource Type = Bed filter missing | Add the filter | Fix on rebuild |
| I4 | Drug ratios > 1 | Drug names not unique | "Drug Label" = name + " (#" + id + ")" | Fix on rebuild |
| I5 | Readmission differs from Python | Denominator differs (all admissions vs eligible) | Label clearly | Documented |
| I6 | Right-edge drop in trends | Discharges trail into Jan 2026 | Limit axis to Dec 2025 | Fix on rebuild |
| I7 | Calculated field name clash | Same name as raw column | Renamed "Efficiency Score (Rolled Up)" | Fixed |

## 5. Known limitations
See `methodology.md` section 7. In short: modeled occupancy, proxy readmission, snapshot-only staff and drug data, single hospital.

## Appendix A — Fresh validation output
(Paste the output of notebook 04 here.)

## Appendix B — Retest results after rebuild
(Fill in the RETEST rows.)

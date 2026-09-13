# Dashboard Storyboard — MedTrack_DV

**Milestone 2: Dashboard Planning (before any Tableau development)**

This storyboard follows the structure required by the project guidance document:
`Dashboard → Purpose → KPIs → Charts → Filters → Interactions`

All four dashboards live in a **single Tableau workbook** (`MedTrack_DV.twbx`) and must feel like one connected application, not four separate files — navigation and global filters are defined once at the end of this document and apply across all four.

---

## Dashboard 1: Hospital Overview

**Purpose:** *"How is the hospital performing overall?"*

**Data source:** `hospital_overview_dataset.csv`, `resource_utilization_dataset.csv`

**KPIs shown (KPI cards, top row):**
- Total Admissions
- Occupancy Rate
- Average Length of Stay
- Readmission Rate
- Bed Utilization Rate

**Charts:**
| Chart | Type | Data |
|---|---|---|
| Monthly Admissions Trend | Line chart | `hospital_overview` grouped by month |
| Admissions vs Discharges | Dual-line / bar chart | derived from `patient_flow_dataset` (Admission vs Discharge events by date) |
| Occupancy Trend | Line chart | `resource_utilization_dataset` grouped by date (hospital-wide) |
| Admissions by Department | Bar chart | `hospital_overview` grouped by `department_name` |
| Admissions by Disease | Bar/Treemap | `hospital_overview` grouped by `disease_name` |

**Filters (local to this dashboard, in addition to global filters below):**
- Date range (default: full period)

**Interactions:**
- Clicking a department bar in "Admissions by Department" filters the KPI cards and trend charts on this same dashboard to that department (Tableau dashboard action, same-dashboard highlight/filter).
- "View Department Analytics" navigation button — jumps to Dashboard 3 carrying the selected department as a filter.

---

## Dashboard 2: Patient Flow

**Purpose:** *"How are patients moving through the hospital?"*

**Data source:** `patient_flow_dataset.csv` (Admission + Discharge events), `hospital_overview_dataset.csv`

**Documented limitation shown in a text/caption box on this dashboard:** HMIS records one ward/bed per admission (no ward-transfer log), so "flow" here is modeled as Admission → Discharge, not a multi-ward journey. This is stated on the dashboard itself, not hidden.

**KPIs shown:**
- Total Admissions
- Total Discharges
- Average Length of Stay
- Peak daily patient load (max concurrent admissions in a day)

**Charts:**
| Chart | Type | Data |
|---|---|---|
| Admission Trend | Line chart | `patient_flow` filtered to movement_type = Admission, by date |
| Discharge Trend | Line chart | `patient_flow` filtered to movement_type = Discharge, by date |
| Patient Volume by Day-of-Week | Bar chart | `patient_flow.day_of_week` |
| Patient Volume by Admission Type | Bar chart | `hospital_overview.admission_type` |
| Length of Stay Distribution | Histogram | `hospital_overview.length_of_stay_days` |
| Peak Patient Load Heatmap | Heatmap (day x hour if available, else day x month) | `patient_flow` |

**Filters:**
- Department
- Admission type
- Date range

**Interactions:**
- Clicking a department in the heatmap/bar chart filters all charts on this dashboard.
- "View Resource Utilization" navigation button — jumps to Dashboard 4 carrying the selected department.

---

## Dashboard 3: Department Analytics

**Purpose:** *"Which departments are performing well and which require attention?"*

**Data source:** `department_analytics_dataset.csv`, `hospital_final_dataset.xlsx` → `Department_KPIs` sheet

**KPIs shown (per department, as a ranked table + cards):**
- Admissions count
- Discharges count
- Readmission Rate
- Average LOS
- Bed Utilization Rate
- **Department Efficiency Score** (headline metric for this dashboard)

**Charts:**
| Chart | Type | Data |
|---|---|---|
| Department Efficiency Score Ranking | Horizontal bar chart, sorted descending | `Department_KPIs` sheet |
| Admissions by Department Over Time | Line chart, one line per department | `department_analytics_dataset` |
| Readmission Rate by Department | Bar chart | `Department_KPIs` sheet |
| Avg LOS by Department (with hospital-wide average reference line) | Bar chart + reference line | `Department_KPIs` sheet, with an annotation on ICU explaining its LOS is clinically expected to be higher (see `kpi_definitions.md`) |
| Department Comparison Table | Text table, sortable | all Department_KPIs columns |

**Filters:**
- Date range
- Department (multi-select, for the trend chart)

**Interactions:**
- Clicking a department in the Efficiency Score ranking filters/highlights that department across the ranking, trend, and comparison table on this dashboard.
- "View Resource Utilization" and "View Patient Flow" navigation buttons carry the selected department forward.

---

## Dashboard 4: Resource Utilization

**Purpose:** *"How efficiently are hospital resources being used?"*

**Data source:** `resource_utilization_dataset.csv` (beds, daily), `resource_utilization_staff_snapshot.csv` (staff, current snapshot — shown separately per documented limitation)

**KPIs shown:**
- Bed Utilization Rate (hospital-wide and by department)
- Total Bed Capacity
- Current Staff Count by role (snapshot, explicitly labeled "current roster" not a trend)

**Charts:**
| Chart | Type | Data |
|---|---|---|
| Daily Bed Occupancy Trend | Line chart | `resource_utilization_dataset`, by date |
| Bed Utilization by Department | Bar chart | `resource_utilization_dataset`, grouped by department |
| Bed Capacity vs Occupied (stacked) | Stacked bar | `resource_utilization_dataset` |
| Current Staff Allocation by Department & Role | Bar chart, clearly titled "Snapshot — not a daily trend" | `resource_utilization_staff_snapshot.csv` |

**Filters:**
- Department
- Date range (applies to bed charts only; staff snapshot chart is not date-filterable, and this is noted in its title/caption)

**Interactions:**
- Clicking a department in "Bed Utilization by Department" filters the occupancy trend and staff allocation chart to that department.

---

## Cross-Dashboard Navigation (applies to all 4)

**Navigation bar** (present on every dashboard, per the project guidance document):
```
Home (Hospital Overview) | Patient Flow | Department Analytics | Resource Utilization
```
Implemented as a set of floating navigation buttons/images with "Go to Sheet" dashboard actions, positioned identically on all four dashboards.

## Global Filters (apply across all dashboards where the field exists)

- **Department** (`department_id` / `department_name`) — the primary cross-dashboard filter, since HMIS has no `hospital_id` (this dataset represents a single hospital).
- **Date range** — applies to all date-based charts.

These are implemented as Tableau filter actions (not just visual filters) set to apply to all sheets using the relevant field, so selecting a department or date range on one dashboard is reflected when navigating to another, per the mentor's requirement that dashboards "feel like one application."

## Example Interaction Flow (per mentor's Section 29 example)

```
Department Analytics
        ↓
User clicks "ICU" in the Efficiency Score ranking
        ↓
Patient Flow dashboard (via navigation button)
        ↓
Shows ICU-filtered admission/discharge trends and LOS distribution
        ↓
Resource Utilization dashboard (via navigation button)
        ↓
Shows ICU-filtered bed occupancy and staff allocation
```

---

## Known Limitations Carried Into Dashboard Design (from `docs/kpi_definitions.md` and `docs/methodology.md`)

1. Single-hospital dataset — no multi-hospital comparison view; "Hospital" filter is not applicable, only "Department".
2. Patient Flow shows a 2-point journey (Admission → Discharge), not multi-ward transfers.
3. Staff Utilization is a current-state snapshot, displayed separately and explicitly labeled, not blended into daily trend charts.
4. ICU's lower Efficiency Score is annotated on-dashboard as a modeling artifact of comparing LOS against a single hospital-wide benchmark, not a genuine operational problem.
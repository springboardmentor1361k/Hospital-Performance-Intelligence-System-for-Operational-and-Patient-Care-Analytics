# MEDTRACK_DV — Hospital Operations & Patient Analytics Dashboard

[![Project Status](https://img.shields.io/badge/Project-Completed%20%7C%20Final%20Submission-success?style=for-the-badge)](#project-status)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Tableau](https://img.shields.io/badge/Tableau-Analytics-E97627?style=flat-square&logo=tableau&logoColor=white)](https://www.tableau.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Version%20Controlled-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/)

> **An integrated hospital analytics system for operational monitoring, patient-flow analysis, department performance evaluation, and resource utilization.**

---

## Overview

**MedTrack_DV** is an end-to-end data analytics and business intelligence project that transforms structured hospital operational data into an integrated Tableau dashboard suite.

The workflow is:

```text
Raw Data
  ↓
Profiling & Cleaning
  ↓
Validation & Standardization
  ↓
Four Analytical Datasets
  ↓
KPI Engineering
  ↓
Tableau Data Model
  ↓
Dashboard Development
  ↓
Integration & QA
```

The project has four analytical perspectives:

1. **Hospital Overview** — executive-level hospital performance
2. **Patient Flow** — patient movements, transfers, and temporal activity
3. **Department Analytics** — department-level operational performance
4. **Resource Utilization** — beds, equipment, and clinical-staff utilization

> MedTrack is an **operational analytics and decision-support system**, not a clinical diagnostic or medical-advice system.

---

## Research Questions

- How can hospital-level operational indicators be consolidated into an executive view?
- How do patient movements, transfers, admissions, and discharges vary across time and departments?
- Which departments differ in occupancy, LOS, readmission, admissions, discharges, and efficiency?
- How effectively are hospital resources utilized, and where are operational pressures concentrated?

---

## Architecture & Dataset Design

The project intentionally preserves the analytical grain of each dataset rather than flattening everything into one table.

| Dataset | Grain | Purpose |
|---|---|---|
| **Hospital Overview** | One row per hospital admission | Admissions, LOS, readmission, patient-level analysis |
| **Patient Flow** | One row per patient movement event | Movement, transfer, shift, temporal analysis |
| **Department Analytics** | One row per hospital + department + day | Department performance and KPI analysis |
| **Resource Utilization** | One row per hospital + department + date + resource type | Capacity, utilization, maintenance analysis |

### Common Keys

`hospital_id` · `department_id` · `patient_id` · `admission_id` · `date`

Tableau relationships/context-specific sources are preferred over unnecessary physical joins to avoid row multiplication and duplicated measures.

---

## Data Preparation

The data pipeline covers:

- Dataset selection and collection
- Data profiling and grain identification
- Duplicate and missing-value handling
- ID/category standardization
- Date standardization
- Derived-field creation
- Analytical dataset construction
- Relationship and referential-integrity validation

Validation focuses on **completeness, uniqueness, consistency, validity, referential integrity, dataset grain, and metric correctness**.

The project guidance targets **>95% completeness** and **<2% missing values after cleaning**.

---

## KPI Engineering

Six mandatory KPIs were engineered and validated.

| KPI | Definition |
|---|---|
| **Total Admissions** | `COUNTD(admission_id)` |
| **Occupancy Rate** | `Occupied Beds / Total Beds × 100` |
| **Average Length of Stay** | `AVERAGE(length_of_stay_days)` |
| **Readmission Rate** | `Readmitted Admissions / Admissions × 100` |
| **Bed Utilization Rate** | `Beds in Use / Available Beds × 100` |
| **Department Efficiency Score** | Composite 0–100 score using occupancy fit, LOS efficiency, readmission performance, and equipment uptime |

The readmission KPI follows the documented **30-day readmission logic**. Detailed KPI methodology is maintained in the project documentation.

---

## Dashboard Suite

### 1. Hospital Overview

**Purpose:** Executive summary of hospital performance.

**KPIs**
- Total Admissions
- Occupancy Rate
- Average Length of Stay
- Readmission Rate
- Bed Utilization Rate
- Department Efficiency

**Views**
- Admissions Over Time
- Admissions by Department
- Admissions vs Discharges
- Operational Snapshot

![Hospital Overview Dashboard](Milestone%203/dashboard/screenshots/hospital_overview.png)

---

### 2. Patient Flow

**Purpose:** Analyze patient movement across departments and time.

**KPIs**
- Total Movements
- Average Time in Department
- Peak Hour Movements
- Average Transfer Time

**Views**
- Patient Movements Over Time
- Movement Type Distribution
- Movements by Shift
- Movements by Day of Week
- Movements by Department

![Patient Flow Dashboard](Milestone%203/dashboard/screenshots/patient_flow.png)

---

### 3. Department Analytics

**Purpose:** Compare department-level operational performance.

**KPIs**
- Total Beds
- Bed Occupancy
- Average Length of Stay
- Readmission Rate
- Efficiency Score

**Views**
- Monthly Bed Occupancy Trend
- Department Efficiency Ranking
- Average LOS by Department
- Readmission Rate by Department
- Admissions vs Discharges

![Department Analytics Dashboard](Milestone%203/dashboard/screenshots/department_analytics.png)

---

### 4. Resource Utilization

**Purpose:** Analyze resource availability, utilization, and operational pressure.

**KPIs**
- Total Resources
- Resource Utilization
- Units in Use
- Units Under Maintenance
- Equipment Downtime
- Overtime Hours

**Views**
- Monthly Resource Utilization Trend
- Average Utilization by Resource Type
- Resource Status by Type
- Equipment Downtime by Department
- Overtime Hours by Department

![Resource Utilization Dashboard](Milestone%203/dashboard/screenshots/resource_utilization.png)

---

## Dashboard Integration

The four dashboards operate as one analytical application:

```text
Hospital Overview
       ↓
Patient Flow
       ↓
Department Analytics
       ↓
Resource Utilization
```

Common/context-specific filters include:

- Hospital
- Department
- Date / Date Range
- Day of Week
- Resource Type
- Department Type

The interaction flow supports operational investigation:

```text
Select Department
      ↓
Inspect Department Performance
      ↓
Examine Patient Flow
      ↓
Inspect Resource Utilization
      ↓
Identify Operational Pressure
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Data Processing | Python |
| Data Manipulation | Pandas, NumPy |
| Storage | CSV, Excel |
| Visualization | Tableau Desktop |
| Dashboard Integration | Tableau Filters, Actions, Navigation |
| Documentation | Markdown |
| Version Control | Git / GitHub |
| Development | GitHub Codespaces |

---

## Repository Structure

```text
Hospital-Performance-Intelligence-System/
├── Milestone 1/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── docs/
│   ├── notebooks/
│   ├── reports/
│   └── scripts/
├── Milestone 2/
│   ├── data/
│   ├── docs/
│   ├── notebooks/
│   ├── reports/
│   └── scripts/
├── Milestone 3/
│   ├── dashboard/
│   │   └── screenshots/
│   ├── docs/
│   └── reports/
├── Milestone 4/
│   ├── docs/
│   └── reports/
└── Final Project/
    ├── Final_Presentation.pptx
    └── Tableau_Dashboard_Link.md
```

---

## Key Documentation

The repository contains supporting documentation for:

- Data dictionary and data profiling
- Dataset validation and data quality
- Data collection and cleaning
- KPI definitions and calculation methodology
- KPI validation
- Dashboard storyboard and planning
- Tableau dashboard development
- QA and dashboard testing
- Dataset sources
- Dashboard user guide
- Final project report

---

## Testing & Validation

Validation covers three main layers:

### Data
- Row counts
- Missing values
- Duplicates
- Primary/foreign keys
- Date validity
- Relationships
- Dataset grain
- Category standardization

### KPIs
- Formula correctness
- Source-field correctness
- Aggregation correctness
- Tableau implementation
- Consistency with documented definitions

### Tableau
- Filters and date ranges
- Dashboard navigation
- Dashboard actions
- Department comparisons
- Cross-dashboard consistency
- Number/percentage formatting
- Axis and label readability
- Layout and visual hierarchy
- Empty-state behavior

The project evaluation criteria target **>95% KPI accuracy**.

---


## Limitations

- The datasets are intended for analytics development and demonstration.
- The project focuses on **hospital operations**, not clinical diagnosis.
- Current analysis is primarily **descriptive**, not predictive.
- KPI outputs depend on documented definitions and dataset assumptions.
- Resource metrics should be interpreted within their defined categories and aggregation levels.
- Dashboard outputs are not medical advice and should not replace clinical judgment.

---

## Future Extensions

Potential next steps include:

- Admission and bed-demand forecasting
- Readmission-risk modeling
- Department workload prediction
- Resource shortage prediction
- Equipment maintenance forecasting
- Staffing demand optimization
- Automated anomaly detection
- Natural-language analytical querying
- Operational alerts
- Scenario-based capacity planning

These extensions could move MedTrack from descriptive BI toward predictive and prescriptive hospital operations analytics.

---

## Conclusion

**MedTrack_DV** demonstrates a complete analytics workflow from raw hospital data to validated KPIs and an integrated Tableau dashboard environment.

The project emphasizes:

1. **Analytical correctness** — documented metrics and appropriate dataset grains.
2. **Operational interpretability** — dashboards designed for monitoring, comparison, and investigation.
3. **Reproducibility** — milestone-based datasets, notebooks, scripts, reports, and documentation.

---


# Author

**Komal Harshita**

*Data Analytics & Business Intelligence | Python | SQL | Power BI | Tableau*

---

<div align="center">

**MEDTRACK_DV**

*Hospital Operations & Patient Analytics Dashboard*

**Built, analyzed and documented by Komal Harshita**

</div>

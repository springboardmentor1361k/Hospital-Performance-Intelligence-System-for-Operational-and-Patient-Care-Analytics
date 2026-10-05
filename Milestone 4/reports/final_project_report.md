# MedTrack_DV — Final Project Report

## Hospital Operations & Patient Analytics Dashboard

**Project:** MedTrack_DV  
**Author:** Komal Harshita  
**Visualization Platform:** Tableau  
**Project Type:** Hospital Operations & Patient Analytics

## 1. Project Overview

MedTrack_DV is a hospital analytics system designed to help hospital management understand operational performance, patient movement, department performance, and resource utilization.

The project transforms healthcare-related datasets into structured analytical datasets, calculates key hospital performance indicators, and presents the results through four interconnected Tableau dashboards:

1. Hospital Overview
2. Patient Flow
3. Department Analytics
4. Resource Utilization

## 2. Project Workflow

```text
Raw Data
    ↓
Data Collection
    ↓
Data Profiling
    ↓
Data Cleaning
    ↓
Data Standardization
    ↓
Data Validation
    ↓
KPI Engineering
    ↓
Tableau Data Model
    ↓
Dashboard Development
    ↓
Dashboard Integration
    ↓
Testing & QA
    ↓
Final Submission
```

## 3. Project Objectives

The system was developed to analyze:

- Patient admissions
- Patient discharges
- Patient movement
- Department performance
- Bed utilization
- Staff utilization
- Equipment utilization
- Hospital capacity
- Readmissions
- Average length of stay
- Department efficiency

## 4. Data Architecture

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per admission |
| Patient Flow | One row per movement event |
| Department Analytics | One hospital + department + day |
| Resource Utilization | One hospital + department + date + resource type |

The different grains were preserved to prevent duplication of measures during analysis.

## 5. Data Preparation

The preparation process included:

- Dataset selection
- Data profiling
- Data cleaning
- Duplicate handling
- Missing-value treatment
- ID standardization
- Department standardization
- Date standardization
- Derived-field creation
- Dataset validation
- Relationship validation

The original raw datasets were preserved separately from processed datasets.

## 6. KPI Engineering

Six mandatory KPIs were developed.

### Total Admissions

`COUNTD(admission_id)`

### Occupancy Rate

`Occupied Beds / Total Beds × 100`

### Average Length of Stay

`AVERAGE(length_of_stay_days)`

### Readmission Rate

`Readmitted Admissions / Admissions × 100`

Readmission is based on an admission occurring within 30 days of the patient's previous discharge.

### Bed Utilization Rate

`Beds in Use / Available Beds × 100`

The resource utilization dataset is filtered to the `Bed` resource type.

### Department Efficiency Score

A 0–100 composite measure incorporating:

- Occupancy fit
- Length-of-stay efficiency
- Readmission
- Equipment uptime

The detailed calculation is documented in `Milestone 2/docs/kpi_definitions.md`.

## 7. Dashboard Development

### Hospital Overview

Provides an executive-level summary of hospital performance.

Key components:

- Total Admissions
- Occupancy Rate
- Average Length of Stay
- Readmission Rate
- Bed Utilization Rate
- Department Efficiency
- Admissions Over Time
- Admissions by Department
- Admissions vs Discharges
- Operational Snapshot

### Patient Flow

Analyzes patient movement through the hospital.

Key components:

- Total Movements
- Average Time in Department
- Peak Hour Movements
- Average Transfer Time
- Patient Movements Over Time
- Movement Type Distribution
- Movements by Shift
- Movements by Day of Week
- Movements by Department

### Department Analytics

Compares departments based on operational performance and patient outcomes.

Key components:

- Total Beds
- Bed Occupancy
- Average Length of Stay
- Readmission Rate
- Efficiency Score
- Monthly Bed Occupancy Trend
- Department Efficiency Ranking
- Average LOS by Department
- Readmission Rate by Department
- Admissions vs Discharges by Department

### Resource Utilization

Analyzes how effectively hospital resources are being used.

Key components:

- Total Resources
- Resource Utilization
- Units in Use
- Units Under Maintenance
- Equipment Downtime
- Overtime Hours
- Monthly Resource Utilization Trend
- Utilization by Resource Type
- Resource Status by Type
- Equipment Downtime by Department
- Overtime Hours by Department

## 8. Dashboard Integration

The four dashboards were designed as one integrated analytical application using:

- Common navigation
- Hospital-level filtering
- Department-level filtering
- Date-based filtering
- Context-specific filtering
- Department comparisons
- Dashboard interactions

## 9. Testing and Validation

Testing covered:

### Data
- Row counts
- Missing values
- Duplicate records
- IDs
- Relationships
- Dates
- Dataset grain

### KPIs
- Formula validation
- Independent calculation comparison
- Tableau value validation

### Dashboards
- Filter behavior
- Navigation
- Dashboard actions
- Department selection
- Hospital selection
- Date filtering
- Visual presentation

Detailed documentation is stored in:

- `Milestone 4/docs/qa_checklist.md`
- `Milestone 4/docs/dashboard_testing_report.md`
- `Milestone 4/docs/testing_report.md`

## 10. Key Analytical Capabilities

The final system enables users to:

- Monitor overall hospital performance
- Track admission and discharge activity
- Analyze patient movement
- Compare departments
- Monitor occupancy
- Analyze readmissions
- Evaluate length of stay
- Compare department efficiency
- Monitor bed utilization
- Analyze equipment downtime
- Monitor staffing and overtime
- Identify resource utilization patterns

## 11. Technology Stack

### Data Processing
- Python
- Pandas
- NumPy

### Data Storage
- CSV
- Excel

### Visualization
- Tableau Desktop
- Tableau Public, where applicable

### Documentation
- Markdown
- GitHub

## 12. Repository Structure

```text
Hospital-Performance-Intelligence-System/
│
├── Milestone 1/
│   ├── data/
│   ├── docs/
│   ├── notebooks/
│   ├── reports/
│   └── scripts/
│
├── Milestone 2/
│   ├── data/
│   ├── docs/
│   ├── notebooks/
│   ├── reports/
│   └── scripts/
│
├── Milestone 3/
│   ├── dashboard/
│   ├── docs/
│   └── reports/
│
├── Milestone 4/
│   ├── docs/
│   └── reports/
│
└── Final Project/
    ├── Final_Presentation.pptx
    └── Tableau_Dashboard_Link.md
```

## 13. Final Deliverables

- Four validated analytical datasets
- Data-cleaning and validation notebooks
- KPI engineering scripts
- Six validated KPIs
- KPI documentation
- Dashboard storyboard
- Four Tableau dashboards
- Integrated Tableau workbook
- QA checklist
- Dashboard testing report
- Dataset source documentation
- Dashboard guide
- Final project documentation
- Final presentation
- Public Tableau dashboard link, where applicable

## 14. Conclusion

MedTrack_DV provides a structured analytical view of hospital operations by combining admission, patient-flow, department, and resource perspectives.

The project follows a complete analytical workflow from data preparation and KPI engineering through Tableau dashboard development, integration, testing, and final documentation.

The resulting dashboard suite is intended to support operational monitoring, department comparison, patient-flow analysis, and resource planning through a single integrated Tableau environment.

## Final Submission Status

| Deliverable | Status |
|---|---|
| Milestone 1 | Complete |
| Milestone 2 | Complete |
| Milestone 3 | Complete |
| Milestone 4 | Final documentation/testing |
| Four dashboards | Complete |
| KPI validation | Complete |
| QA documentation | Complete |
| Final Tableau workbook | To be added |
| Tableau Public link | To be added |
| Final presentation | To be added |

**Project Status: Ready for Final Submission**

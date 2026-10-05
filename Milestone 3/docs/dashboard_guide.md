# MedTrack_DV — Dashboard Guide

## 1. Overview

MedTrack_DV is a Hospital Operations & Patient Analytics Dashboard designed to provide an integrated view of hospital performance, patient movement, department operations, and resource utilization.

The final Tableau solution consists of four interconnected dashboards:

1. Hospital Overview
2. Patient Flow
3. Department Analytics
4. Resource Utilization

The dashboards are designed as one analytical system rather than four independent dashboards.

---

## 2. Dashboard Navigation

The dashboard suite uses a common navigation structure:

- Hospital Overview
- Patient Flow
- Department Analytics
- Resource Utilization

Users can move between dashboards using the navigation controls provided within the Tableau workbook.

---

# 3. Hospital Overview

### Purpose

The Hospital Overview dashboard provides an executive-level summary of overall hospital performance.

### Key Questions

- How is the hospital performing overall?
- How many admissions are being handled?
- What is the current occupancy level?
- How long are patients staying?
- What is the readmission rate?
- How efficiently are hospital resources being utilized?

### KPI Cards

The dashboard includes:

- Total Admissions
- Occupancy Rate
- Average Length of Stay
- Readmission Rate
- Bed Utilization Rate
- Department Efficiency Score

### Main Visualizations

- Admissions Over Time
- Admissions by Department
- Admissions vs Discharges
- Operational Snapshot

### Filters

- Department Name
- Hospital Name
- Date Range

### Intended Users

- Hospital administrators
- Operations managers
- Hospital management

---

# 4. Patient Flow

### Purpose

The Patient Flow dashboard analyzes how patients move through the hospital and identifies periods of higher patient activity.

### Key Questions

- How many patient movements are occurring?
- What types of movements are most common?
- Which departments experience the highest movement?
- When is patient activity highest?
- How long do patients spend in departments?

### KPI Cards

The dashboard includes:

- Total Movements
- Average Time in Department
- Peak Hour Movements
- Average Transfer Time

### Main Visualizations

- Patient Movements Over Time
- Movement Type Distribution
- Movements by Shift
- Movements by Day of Week
- Movements by Department

### Filters

- Department Name
- Day of Week
- Movement Date / Date Range

### Movement Types

The dashboard can analyze movement categories including:

- Admission
- Discharge
- Department Change
- Transfer
- ICU Transfer

### Intended Users

- Operations managers
- Clinical managers
- Patient-flow teams

---

# 5. Department Analytics

### Purpose

The Department Analytics dashboard compares hospital departments based on operational performance, capacity, patient volume, outcomes, and efficiency.

### Key Questions

- Which departments have the highest workload?
- Which departments have higher occupancy?
- Which departments have longer patient stays?
- Which departments have higher readmission rates?
- Which departments are performing efficiently?

### KPI Cards

The dashboard includes:

- Total Beds
- Bed Occupancy
- Average Length of Stay
- Readmission Rate
- Efficiency Score

### Main Visualizations

- Monthly Bed Occupancy Trend
- Department Efficiency Score
- Average Length of Stay by Department
- Readmission Rate by Department
- Admissions vs Discharges by Department

### Filters

- Department Name
- Hospital Name
- Department Type
- Date Range

### Intended Users

- Department managers
- Hospital operations teams
- Clinical management

---

# 6. Resource Utilization

### Purpose

The Resource Utilization dashboard evaluates how effectively hospital beds, equipment, and clinical staff are being utilized.

### Key Questions

- How efficiently are resources being used?
- Which resource types have higher utilization?
- How many units are currently in use?
- How many resources are under maintenance?
- Which departments have higher equipment downtime?
- Which departments have higher overtime requirements?

### KPI Cards

The dashboard includes:

- Total Resources
- Resource Utilization
- Units in Use
- Units Under Maintenance
- Equipment Downtime
- Overtime Hours

### Main Visualizations

- Monthly Resource Utilization Trend
- Average Utilization by Resource Type
- Resource Status by Type
- Equipment Downtime of Top Departments
- Overtime Hours by Department

### Filters

- Department Name
- Hospital Name
- Resource Type

### Resource Types

The resource dataset contains:

- Beds
- Equipment
- Clinical Staff

### Intended Users

- Operations managers
- Resource managers
- Hospital administrators

---

# 7. Global Filtering

Where applicable, the dashboard suite supports common analytical dimensions such as:

- Hospital
- Department
- Date / Date Range

Context-specific filters are provided where required by the individual dashboard.

Filtering should update the relevant dashboard views while preserving the analytical meaning of each dataset.

---

# 8. Dashboard Integration

The four dashboards are intended to function as a single application.

The integration includes:

- Dashboard navigation
- Common filtering concepts
- Department-level analysis
- Hospital-level analysis
- Date-based analysis
- Dashboard actions where applicable

The project follows the recommended Tableau architecture of keeping the four analytical datasets at their respective grains rather than blindly combining all datasets into one table.

---

# 9. Dataset Grains

The dashboards use four analytical datasets.

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per hospital admission |
| Patient Flow | One row per patient movement event |
| Department Analytics | One row per hospital + department + day |
| Resource Utilization | One row per hospital + department + date + resource type |

Because these datasets have different grains, measures should not be duplicated through unnecessary joins.

---

# 10. KPI Definitions

The six mandatory KPIs are:

| KPI | Definition |
|---|---|
| Total Admissions | COUNTD(admission_id) |
| Occupancy Rate | Occupied Beds / Total Beds × 100 |
| Average Length of Stay | AVERAGE(length_of_stay_days) |
| Readmission Rate | Readmitted Admissions / Admissions × 100 |
| Bed Utilization Rate | Beds in Use / Available Beds × 100 |
| Department Efficiency Score | Composite 0–100 efficiency score |

Detailed formulas and calculation methodology are documented separately in:

`Milestone 2/docs/kpi_definitions.md`

---

# 11. Recommended Usage

For an overall hospital assessment:

**Hospital Overview → Department Analytics → Resource Utilization**

For patient movement analysis:

**Patient Flow → Department Analytics**

For resource planning:

**Resource Utilization → Department Analytics**

The dashboards should be used together to move from overall hospital performance to department-level and resource-level analysis.

---

# 12. Tableau Workbook

The final integrated Tableau workbook contains the four dashboards:

`MedTrack_DV.twbx`

The workbook should be treated as the primary visualization and dashboard-delivery artifact for the project.

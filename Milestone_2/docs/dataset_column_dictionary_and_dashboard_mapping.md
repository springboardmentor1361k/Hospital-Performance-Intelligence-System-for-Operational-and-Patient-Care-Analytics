# MedTrack Hospital Performance Intelligence System
## Dataset Column Dictionary & Tableau Dashboard Implementation Guide

This reference document details all operational datasets, column definitions, data types, statistical profiles, grain specifications, and their exact mappings to the 3 executive Tableau dashboards.

---

## 1. Data Model Architecture & Grain Specifications

To avoid Cartesian multiplication and inflated metric counts in Tableau, datasets are structured across distinct grains:

```text
┌───────────────────────────────────────────────────────────────┐
│                     TABLEAU DATA MODEL                        │
└───────────────────────────────────────────────────────────────┘
  [Patient Level Grain]                     [Aggregated Operations]
   hospital_overview_dataset                 department_analytics_dataset
   (1 row = 1 admission, 1,000 rows)         (1 row = 1 dept × week, 208 rows)
           │                                                │
           │ (1:2 relationship on admission_id)            │
           ▼                                                ▼
   patient_flow_dataset                      resource_utilization_dataset
   (1 row = 1 movement, 2,000 rows)          (1 row = 1 dept × week × role, 628 rows)
```

> **Design Rule**: Do NOT physically flat-join all four tables into one flat CSV. Maintain them as separate logical tables/relationships in Tableau, joining `hospital_overview` to `patient_flow` via `admission_id`, and linking departmental metrics via `department_name` and `week`.

---

## 2. Processed Analytical Tables (`Milestone_1/data/processed/`)

### Table 1: `hospital_overview_dataset.csv`
* **File Location**: `Milestone_1/data/processed/hospital_overview_dataset.csv`
* **Grain**: 1 row = 1 Inpatient Admission
* **Total Volume**: 1,000 rows × 14 columns
* **Dashboard Feeds**:
  - **Dashboard 1**: Inpatient throughput volume, ALOS target bullet graph, intake channel flows.
  - **Dashboard 2**: Demographics pyramid, patient age distribution, length of stay box-and-whisker.

| Column Name | Data Type | Tableau Classification | Sample / Range | Business Description & Dashboard Usage |
| :--- | :--- | :--- | :--- | :--- |
| `admission_id` | String | Dimension (Primary Key) | `ADM-09484753` | Unique admission identifier. Used for `COUNTD(admission_id)` as Total Admissions. |
| `patient_id` | String | Dimension (Foreign Key) | `PAT-09484753` | Unique patient identifier. |
| `name` | String | Dimension (Attribute) | `Richard Rodriguez` | Inpatient full name. Used in case-level drilldown tooltips. |
| `age` | Integer | Dimension / Measure | `0` to `119` years | Patient age. Create calculated bins: `<18`, `18-45`, `46-65`, `65+`. |
| `department_name` | String | Dimension (Categorical) | `emergency`, `icu`, `surgery`, `general_medicine` | Clinical service ward. Primary global slicer and treemap dimension. |
| `admission_date` | Date | Dimension (Temporal) | `2025-01-01` to `2025-12-31` | Arrival timestamp. Drives time-series filters, monthly trends, and intake horizon. |
| `discharge_date` | Date | Dimension (Temporal) | `2025-01-02` to `2026-01-07` | Patient departure timestamp. |
| `length_of_stay_days` | Integer | Measure (Continuous) | `1` to `14` days | Stay duration (`discharge_date - admission_date`). Used for ALOS benchmarks and outlier detection. |
| `patient_satisfaction_score`| Integer | Measure (Continuous) | `60` to `99` (Mean: 80.0) | Clinical care satisfaction rating (0–100 scale). |
| `year` | Integer | Dimension (Temporal) | `2025` | Operational calendar year. Global dashboard filter. |
| `month` | Integer | Dimension (Temporal) | `1` to `12` | Calendar intake month. Seasonal trend slicer. |
| `quarter` | Integer | Dimension (Temporal) | `1` to `4` | Calendar quarter (Q1 to Q4). |
| `day_of_week` | String | Dimension (Temporal) | `Monday` to `Sunday` | Day of intake. Used for weekday surge pattern analysis. |
| `readmission_flag` | Integer | Measure / Flag | `0` (Binary 0/1) | Indicates 30-day unscheduled readmission. |

---

### Table 2: `department_analytics_dataset.csv`
* **File Location**: `Milestone_1/data/processed/department_analytics_dataset.csv`
* **Grain**: 1 row = 1 Department × 1 Operational Week
* **Total Volume**: 208 rows × 12 columns (4 departments × 52 weeks)
* **Dashboard Feeds**:
  - **Dashboard 1**: 52-week departmental sparklines, demand vs capacity horizon.
  - **Dashboard 3**: Bed capacity thresholds, weekly utilization trends.

| Column Name | Data Type | Tableau Classification | Sample / Range | Business Description & Dashboard Usage |
| :--- | :--- | :--- | :--- | :--- |
| `year` | Integer | Dimension (Temporal) | `2025` | Operational reporting year. |
| `week` | Integer | Dimension (Temporal) | `1` to `52` | Operational week number. Primary dimension for time-series area charts and sparklines. |
| `department_name` | String | Dimension (Categorical) | `emergency`, `icu`, `surgery`, `general_medicine` | Department identifier. |
| `patients_admitted_count` | Integer | Measure (Volume) | `0` to `10` per week | Number of weekly patient admissions in that department. |
| `avg_length_of_stay_days` | Float | Measure (Continuous) | `1.00` to `14.00` days | Weekly average duration of stay. |
| `avg_satisfaction_score` | Float | Measure (Continuous) | `60.00` to `99.00` | Weekly average patient satisfaction score. |
| `patients_discharged_count`| Integer | Measure (Volume) | `0` to `10` per week | Weekly throughput of discharged patients. |
| `readmission_count` | Integer | Measure (Volume) | `0` | Count of 30-day readmissions. |
| `readmission_rate_pct` | Float | Measure (Percentage) | `0.0%` | Readmission rate percentage. |
| `available_beds_ref` | Integer | Measure (Capacity) | `16` to `39` beds | Assigned operational bed baseline. |
| `event_ref` | String | Dimension (Event Flag) | `none`, `flu_outbreak`, `strike` | Clinical and operational anomaly flags. |
| `bed_occupancy_rate_ref_pct`| Float | Measure (Percentage) | `0.0%` to `46.4%` | Derived weekly bed occupancy rate percentage. |

---

### Table 3: `patient_flow_dataset.csv`
* **File Location**: `Milestone_1/data/processed/patient_flow_dataset.csv`
* **Grain**: 1 row = 1 Patient Movement Event
* **Total Volume**: 2,000 rows × 10 columns (2 movement events per patient)
* **Dashboard Feeds**:
  - **Dashboard 2**: Patient progression flow, stage-based care transitions, stay duration by stage.

| Column Name | Data Type | Tableau Classification | Sample / Range | Business Description & Dashboard Usage |
| :--- | :--- | :--- | :--- | :--- |
| `movement_id` | String | Dimension (Primary Key) | `MOV-00001` to `MOV-02000` | Unique movement stage event ID. |
| `admission_id` | String | Dimension (Foreign Key) | `ADM-003ce690` | Relational join key linking to `hospital_overview_dataset`. |
| `patient_id` | String | Dimension (Foreign Key) | `PAT-003ce690` | Patient identifier. |
| `department_name` | String | Dimension (Categorical) | `emergency`, `icu`, `surgery`, `general_medicine` | Service location during movement. |
| `year` | Integer | Dimension (Temporal) | `2025` | Movement calendar year. |
| `month` | Integer | Dimension (Temporal) | `1` to `12` | Movement calendar month. |
| `day_of_week` | String | Dimension (Temporal) | `Monday` to `Sunday` | Day of movement occurrence. |
| `movement_type` | String | Dimension (Flow Step) | `Admission`, `Discharge` | Stage in clinical trajectory (maps origin → destination). |
| `movement_date` | Date | Dimension (Temporal) | `2025-01-01` to `2026-01-07` | Exact event date. |
| `duration_in_department_hours`| Float | Measure (Continuous) | `24.0` to `336.0` hours | Department stay duration in hours (`length_of_stay_days × 24`). |

---

### Table 4: `resource_utilization_dataset.csv`
* **File Location**: `Milestone_1/data/processed/resource_utilization_dataset.csv`
* **Grain**: 1 row = 1 Department × 1 Week × 1 Resource Type
* **Total Volume**: 628 rows × 8 columns
* **Dashboard Feeds**:
  - **Dashboard 3**: Workforce stress index, bed utilization bullet charts, shift saturation.

| Column Name | Data Type | Tableau Classification | Sample / Range | Business Description & Dashboard Usage |
| :--- | :--- | :--- | :--- | :--- |
| `resource_utilization_id` | String | Dimension (Primary Key) | `RES-00001` to `RES-00628` | Unique resource log identifier. |
| `week` | Integer | Dimension (Temporal) | `1` to `52` | Operational week number. |
| `department_name` | String | Dimension (Categorical) | `emergency`, `icu`, `surgery`, `general_medicine` | Clinical service ward. |
| `resource_type` | String | Dimension (Filter/Group) | `doctor`, `nurse`, `bed` | Specific resource being tracked. |
| `resource_category` | String | Dimension (Parameter) | `staff`, `bed` | High-level grouping. Drives Tableau parameter to toggle between Beds and Staff. |
| `total_units_available` | Integer | Measure (Capacity) | `1` to `39` units | Available operational units in service. |
| `units_in_use` | Integer | Measure (Utilization) | `1` to `39` units | Active units currently deployed. |
| `utilization_rate_pct` | Float | Measure (Percentage) | `25.0%` to `100.0%` | Resource utilization percentage (`units_in_use / total_units × 100`). |

---

## 3. Milestone 2 Scorecards & KPI Benchmarks (`Milestone_2/data/`)

### Table 5: `department_kpi_summary_milestone2.csv`
* **File Location**: `Milestone_2/data/department_kpi_summary_milestone2.csv`
* **Grain**: 1 row = 1 Department (4 departments)
* **Dashboard Feeds**: **Dashboard 3 — 4-Quadrant Strategic Efficiency Matrix**

| Department | Admissions | ALOS (d) | Bed Util (%) | Turnaway Rate (%) | Demand Fulfillment (%) | Staff Util (%) | Morale | Satisfaction | Efficiency Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Emergency** | 263 | 7.16 | **100.00%** | **80.87%** | 19.13% | 89.42% | 73.56 | 77.88 | **53.33 / 100** |
| **Surgery** | 254 | 7.87 | 88.19% | 24.77% | 75.23% | 89.82% | 72.88 | 80.57 | **74.36 / 100** |
| **General Medicine**| 242 | 7.00 | 97.32% | 45.39% | 54.61% | 87.66% | 71.92 | 80.45 | **67.85 / 100** |
| **ICU** | 241 | 7.61 | 84.38% | 17.87% | 82.13% | 89.03% | 71.92 | 81.16 | **77.64 / 100** |

---

### Table 6: `hospital_kpi_scorecard_milestone2.csv`
* **File Location**: `Milestone_2/data/hospital_kpi_scorecard_milestone2.csv`
* **Grain**: 1 row = 1 Key Performance Indicator (11 KPIs)
* **Dashboard Feeds**: Header KPI Cards and Executive Banners across all 3 dashboards.

| KPI ID | KPI Name | Category | Value | Unit | Target Benchmark | Novel / Differentiated |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **KPI-01** | Total Admissions | Volume & Demand | 1,000 | Patients | 1,000 | Standard |
| **KPI-02** | Average Length of Stay (ALOS)| Operational Flow | 7.41 | Days | < 7.00 Days | Standard |
| **KPI-03** | Bed Occupancy Rate | Capacity & Utilization | 20.47 | % | 80.0% – 85.0% | Standard |
| **KPI-04** | Bed Utilization Rate | Capacity & Utilization | 92.47 | % | 85.0% | Standard |
| **KPI-05** | 30-Day Readmission Rate | Clinical Care Quality | 0.00 | % | < 5.0% | Standard |
| **KPI-06** | Department Efficiency Score | Operational Flow | 88.45 | Score (/100) | > 80.00 | Standard |
| **KPI-07** | **Patient Turnaway Rate** | Volume & Demand | **56.64** | **%** | **< 20.0%** | **Novel KPI 1** |
| **KPI-08** | **Demand Fulfillment Rate** | Volume & Demand | **43.36** | **%** | **> 80.0%** | **Novel KPI 2** |
| **KPI-09** | **Net Patient Satisfaction** | Clinical Care Quality | **80.00** | **Score (/100)**| **> 85.00** | **Novel KPI 3** |
| **KPI-10** | **Caregiver Morale Index** | Workforce & Efficiency| **72.57** | **Score (/100)**| **> 75.00** | **Novel KPI 4** |
| **KPI-11** | **Clinical Workforce Stress** | Workforce & Efficiency| **88.98** | **%** | **< 80.0%** | **Novel KPI 5** |

---

## 4. Key Raw Source Demand Fields (`Milestone_1/data/raw/services_weekly.csv`)
*Use these fields when generating the **Demand vs Capacity Horizon Area Ribbon** on Dashboard 1:*
* `patients_request`: Inbound community patient admission requests (Total: 13,493).
* `patients_admitted`: Admitted patient count (Total: 5,851).
* `patients_refused`: Turned away patient requests due to bed/staff exhaustion (Total: 7,642).
* `staff_morale`: Weekly caregiver morale score (0–100).

---

## 5. Dashboard Visual Mapping Reference

| Dashboard | Visual Name | Recommended Chart Type | Primary Data Fields Used |
| :--- | :--- | :--- | :--- |
| **Dashboard 1** | Demand vs Capacity Horizon | Dual-Axis Area & Horizon Ribbon | `week`, `patients_request`, `patients_admitted`, `patients_refused` |
| **Dashboard 1** | Department Intake Volume | Treemap with Sparklines | `department_name`, `admission_id (COUNTD)`, `week` |
| **Dashboard 1** | Hospital Bed Allocation | 100-Mark Waffle Matrix & Gauge | `department_name`, `bed_utilization_pct` |
| **Dashboard 1** | ALOS Target Benchmark | Clinical Target Bullet Graph | `department_name`, `length_of_stay_days (AVG)`, CMS Target: 7.0d |
| **Dashboard 2** | Clinical Progression Pathway | Patient Acuity Flow | `movement_type`, `department_name`, `admission_id (COUNTD)` |
| **Dashboard 2** | Length of Stay Variance | Box-and-Whisker Distribution | `department_name`, `length_of_stay_days` |
| **Dashboard 2** | Demographic Urgency | Population Age Pyramid | `age (binned)`, `admission_id (COUNTD)`, `department_name` |
| **Dashboard 3** | Strategic Efficiency Matrix | 4-Quadrant Scatter Plot | X: `bed_utilization_pct`, Y: `demand_fulfillment_pct`, Size: `staff_utilization_pct` |
| **Dashboard 3** | Capacity Safety Thresholds | Threshold Bullet Chart | `resource_category`, `utilization_rate_pct`, Bands: 80%/85%/95% |
| **Dashboard 3** | Ward Strain Temporal Grid | Heatmap Matrix | `day_of_week`, `resource_type`, `utilization_rate_pct` |

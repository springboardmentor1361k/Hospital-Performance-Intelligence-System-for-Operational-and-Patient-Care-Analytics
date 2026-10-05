# MedTrack_DV — Dashboard Testing Report

## 1. Objective

This report documents testing of the MedTrack_DV Hospital Operations & Patient Analytics Dashboard.

Testing verified:

- KPI calculations
- Dashboard functionality
- Filters
- Navigation
- Dashboard interactions
- Visual presentation
- Cross-dashboard consistency

## 2. Dashboards Tested

1. Hospital Overview
2. Patient Flow
3. Department Analytics
4. Resource Utilization

## 3. Data Validation

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per admission |
| Patient Flow | One row per movement event |
| Department Analytics | One hospital + department + day |
| Resource Utilization | One hospital + department + date + resource type |

The different grains were considered during dashboard development to avoid unnecessary duplication of measures.

## 4. KPI Testing

### Total Admissions
`COUNTD(admission_id)`

Source: `hospital_overview_dataset.csv`

### Occupancy Rate
`Occupied Beds / Total Beds × 100`

Source: `department_analytics_dataset.csv`

### Average Length of Stay
`AVERAGE(length_of_stay_days)`

Source: `hospital_overview_dataset.csv`

### Readmission Rate
`Readmitted Admissions / Admissions × 100`

Source: `hospital_overview_dataset.csv`

### Bed Utilization Rate
`Beds in Use / Available Beds × 100`

Source: `resource_utilization_dataset.csv`

Resource type: `Bed`

### Department Efficiency Score

A 0–100 composite based on occupancy fit, LOS efficiency, readmission, and equipment uptime.

Source: `department_analytics_dataset.csv`

## 5. Functional Testing

### Filters

Tested:

- Hospital
- Department
- Department Type
- Date Range
- Day of Week
- Movement Type
- Resource Type

**Result: PASS**

### Navigation

Navigation between all four dashboards was tested.

**Result: PASS**

### Dashboard Actions

Tested:

- Department selection
- Hospital selection
- Filtering
- Cross-dashboard context where implemented

**Result: PASS**

## 6. Dashboard Testing

### Hospital Overview
- KPI cards
- Admissions trend
- Admissions by department
- Admissions vs discharges
- Operational snapshot

**Result: PASS**

### Patient Flow
- Movement KPIs
- Movement trend
- Movement type distribution
- Shift analysis
- Day-of-week analysis
- Department movement

**Result: PASS**

### Department Analytics
- Department KPIs
- Occupancy trend
- Efficiency ranking
- LOS by department
- Readmission by department
- Admissions vs discharges

**Result: PASS**

### Resource Utilization
- Resource KPIs
- Utilization trend
- Utilization by resource type
- Resource status
- Equipment downtime
- Overtime

**Result: PASS**

## 7. Visual Validation

Reviewed for:

- Clear titles
- Consistent typography
- Consistent navigation
- Readable KPI cards
- Meaningful labels
- Appropriate chart types
- Consistent layout
- Filter visibility
- No major overlapping elements
- No major blank visualizations

**Result: PASS**

## 8. Final Result

| Area | Result |
|---|---|
| Data structure | PASS |
| KPI calculations | PASS |
| Hospital Overview | PASS |
| Patient Flow | PASS |
| Department Analytics | PASS |
| Resource Utilization | PASS |
| Filters | PASS |
| Navigation | PASS |
| Dashboard interactions | PASS |
| Visual presentation | PASS |

**Overall Result: PASS — Dashboard suite ready for final delivery.**

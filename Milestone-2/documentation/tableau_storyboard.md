# Tableau Storyboard

## Hospital Performance Intelligence System

---

## 1. Purpose

The Tableau storyboard will present hospital operational and patient-care analytics using the prepared analytical datasets and calculated KPIs.

The storyboard will help hospital administrators understand admission trends, patient flow, department performance and resource utilization.

---

## 2. Story Point 1: Hospital Overview

### Objective

Provide a high-level summary of hospital performance.

### KPIs

- Total Admissions
- Average Length of Stay
- Occupancy Rate
- Bed Utilization Rate
- Department Efficiency Score
- Readmission Rate

### Planned Visualizations

- KPI cards for major hospital indicators
- Monthly admission trend line chart
- Admissions by department bar chart
- Admission type distribution
- Admission status summary

### Filters

- Admission Date
- Department
- Admission Type
- Gender
- Admission Status

### Expected Insight

This page will help identify the overall hospital workload, admission patterns and general operational performance.

The Readmission Rate will be displayed as unavailable until the suitable readmission dataset is integrated.

---

## 3. Story Point 2: Patient Flow Analysis

### Objective

Analyze patient movement through admission and discharge events.

### Planned Visualizations

- Daily admission and discharge trend
- Admission versus discharge comparison
- Patient flow by department
- Daily patient movement distribution
- Peak admission and discharge periods

### Filters

- Date
- Department
- Event Type
- Admission Type

### Expected Insight

This page will help identify patient flow patterns, high-traffic periods and departments experiencing increased patient movement.

---

## 4. Story Point 3: Department Analytics

### Objective

Compare the workload and performance of hospital departments.

### Planned Visualizations

- Admissions by department
- Average length of stay by department
- Department efficiency score ranking
- Patient-days by department
- Admissions per available bed

### Filters

- Department
- Department Type
- Date
- Ward

### Expected Insight

This page will help identify high-performing departments, departments with high patient loads and areas requiring operational improvement.

---

## 5. Story Point 4: Resource Utilization

### Objective

Evaluate the availability and utilization of hospital beds and other resources.

### Planned Visualizations

- Total beds by department
- Used beds versus available beds
- Bed utilization rate by department
- Patient-days by department
- Occupancy rate comparison

### Filters

- Department
- Ward
- Bed Status
- Date

### Expected Insight

This page will support resource planning and help identify departments with high or low bed utilization.

---

## 6. Story Navigation

The storyboard will follow this sequence:

1. Hospital Overview
2. Patient Flow Analysis
3. Department Analytics
4. Resource Utilization

The sequence begins with a general hospital summary and gradually moves toward detailed operational analysis.

---

## 7. Dashboard Design Principles

- Use a clean and consistent layout.
- Use KPI cards for important numerical indicators.
- Use suitable charts for trends and comparisons.
- Use consistent colors for admission and discharge events.
- Provide filters for interactive analysis.
- Use readable titles, labels and legends.
- Avoid unnecessary visual elements.
- Ensure the dashboard is understandable to hospital administrators.

---

## 8. Data Sources

The storyboard will use the following processed datasets:

- `hospital_overview_dataset.csv`
- `patient_flow_dataset.csv`
- `department_analytics_dataset.csv`
- `resource_utilization_dataset.csv`
- `kpi_summary.csv`
- `department_kpi_summary.csv`

---

## 9. Validation Considerations

The dashboard values will be checked against the KPI calculation outputs generated using Python.

The following indicators will be validated:

- Total Admissions
- Average Length of Stay
- Occupancy Rate
- Bed Utilization Rate
- Department Efficiency Score

The Readmission Rate will remain marked as unavailable until the approved patient readmission dataset is collected and integrated.

---

## 10. Expected Outcome

The Tableau storyboard will provide a structured plan for developing an interactive hospital performance dashboard.

It will help transform the prepared datasets into meaningful visual insights for hospital operations, patient flow monitoring, departmental comparison and resource planning.
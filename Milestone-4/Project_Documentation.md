# Project Documentation
## Hospital Performance Intelligence System (MedTrack_DV)

## 1. Introduction

The Hospital Performance Intelligence System is a data visualization project designed to explore hospital operations and patient analytics. It uses hospital datasets and interactive Tableau dashboards to present information about admissions, patient flow, department activity, and resource utilization.

## 2. Project Objectives

- Analyze hospital admission and discharge patterns.
- Present key hospital performance indicators.
- Explore patient movement and admission types.
- Compare department admissions and billing.
- Examine resource utilization and availability.
- Provide a unified dashboard interface for exploring hospital data.

## 3. Tools and Technologies

| Tool or Technology | Purpose |
|---|---|
| Python | Data processing and KPI preparation |
| Pandas | Dataset cleaning and analysis |
| Excel | Storage and organization of prepared datasets |
| Tableau Public | Interactive dashboards and data visualization |
| Jupyter Notebook | Data exploration and cleaning |
| Git and GitHub | Version control and project collaboration |
| Markdown | Project documentation |

## 4. Dataset Description

The project uses structured hospital data covering multiple operational areas.

| Dataset | Purpose |
|---|---|
| Patient | Patient demographic information |
| Admission | Admission and discharge information |
| Bed | Bed information and status |
| Ward | Ward information and classification |
| Department | Hospital department details |
| Doctor | Doctor information |
| Billing | Admission billing records |
| Billing Detail | Itemized billing information |
| Diagnostic Test | Diagnostic test details |
| Patient Diagnostic | Patient diagnostic records |
| Prescription | Prescription information |
| Patient Insurance | Patient insurance information |
| Insurance Provider | Insurance provider details |
| Staff Assignment | Staff assignment information |

The prepared datasets are organized into hospital overview, patient flow, department analytics, resource utilization, and KPI summary outputs.

## 5. Data Processing Workflow

1. Collect and organize the raw hospital datasets.
2. Inspect dataset columns, data types, missing values, and record counts.
3. Clean and prepare the data for analysis.
4. Generate analytical datasets for different hospital operations.
5. Calculate and summarize available key performance indicators.
6. Export prepared data for use in Tableau.
7. Develop dashboards to visualize hospital performance.

## 6. Dashboard Description

### 6.1 Home Dashboard

Provides the project title, introduction, and navigation to the four main dashboards.

### 6.2 Hospital Overview Dashboard

Displays hospital-wide indicators, including total admissions, average length of stay, bed utilization rate, occupancy rate, and department efficiency score. Monthly admission and discharge trends provide an overview of hospital activity.

### 6.3 Patient Flow Dashboard

Displays patient movement trends, monthly discharges, and the distribution of elective and emergency admissions.

### 6.4 Department Analytics Dashboard

Presents department-level admissions and billing analysis to support comparisons of hospital activity.

### 6.5 Resource Utilization Dashboard

Presents resource utilization analysis and department-wise resource availability.

## 7. Key Performance Indicators

| KPI | Displayed Value | Description |
|---|---:|---|
| Total Admissions | 45,000 | Total admission records represented in the prepared dataset |
| Average Length of Stay | 5.155 days | Average length of stay displayed in Tableau |
| Bed Utilization Rate | 34.94% | Utilization value reported in the KPI summary |
| Occupancy Rate | 25.36% | Occupancy value reported in the KPI summary |
| Department Efficiency Score | 90.13 | Department efficiency value reported in the KPI summary |
| Readmission Rate | Not available | Not established in the current KPI summary |

The occupancy rate, bed utilization rate, and department efficiency score are displayed as fixed values in the current Tableau workbook. Their formulas and underlying definitions should be validated before interpreting them as dynamic calculations. Readmission rate requires an appropriate definition and supporting patient admission history.

## 8. Project Deliverables

The project is organized into milestone folders covering data preparation, KPI generation, dashboard integration, and quality assurance.

Key deliverables include:

- Prepared hospital datasets.
- KPI generation scripts and summary files.
- Hospital final dataset workbook.
- Tableau dashboard workbooks.
- Dashboard integration report.
- QA checklist.
- Dashboard testing report.
- Final project documentation.

## 9. Limitations

- Readmission rate is not established in the current KPI summary.
- Some displayed KPI values are fixed values rather than dynamically calculated Tableau measures.
- Resource availability figures require validation against the source data.
- Dashboard conclusions depend on the quality, completeness, and definitions of the available datasets.

## 10. Future Enhancements

- Implement dynamic KPI calculations within Tableau.
- Add validated readmission analysis using patient admission history.
- Improve resource availability calculations using appropriate bed-level records.
- Expand interactive filtering and cross-dashboard analysis.
- Add trend comparisons across years and departments.
- Improve automated data validation and refresh workflows.

## 11. Conclusion

The Hospital Performance Intelligence System provides an interactive interface for exploring hospital operations and patient analytics. Its dashboards summarize hospital activity, patient flow, department performance, and resource utilization.

The project demonstrates the use of data preparation, KPI summaries, and visualization to support hospital performance analysis. Further validation of selected KPI calculations and resource measures will improve the reliability of the system.
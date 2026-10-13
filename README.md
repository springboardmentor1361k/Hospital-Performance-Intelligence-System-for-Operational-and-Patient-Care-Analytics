# Hospital Performance Intelligence System

### MedTrack_DV — Hospital Operations and Patient Care Analytics

## 1. Project Overview

The Hospital Performance Intelligence System is a data visualization project developed to analyze hospital operations and patient analytics. It transforms structured hospital datasets into interactive Tableau dashboards that help users explore admission patterns, patient flow, department activity, and resource utilization.

The project combines data preparation, KPI summaries, and interactive visualizations to present hospital information in an accessible format.

## 2. Objectives

- Analyze hospital admissions and discharge patterns.
- Present important hospital performance indicators.
- Explore elective and emergency admission distributions.
- Compare department admissions and billing activity.
- Examine resource utilization and availability.
- Provide an interactive dashboard suite for exploring hospital operations.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and KPI generation |
| Pandas | Data cleaning and analysis |
| Jupyter Notebook | Data exploration and preparation |
| Excel | Prepared datasets and KPI summaries |
| Tableau Public | Interactive dashboards and visualizations |
| Git and GitHub | Version control and project organization |
| Markdown | Project documentation |

## 4. Dashboard Suite

The published Tableau workbook contains a Home page and four main dashboards.

### Home Dashboard
Provides the project introduction and navigation to the four main dashboards.

### Hospital Overview
Displays hospital-wide KPI cards and monthly admission and discharge trends.

### Patient Flow Dashboard
Presents patient movement trends, monthly discharges, and elective versus emergency admissions.

### Department Analytics Dashboard
Explores department admissions and billing activity.

### Resource Utilization Dashboard
Presents resource utilization analysis and department-wise resource availability.

## 5. Key Performance Indicators

| KPI | Displayed Value |
|---|---:|
| Total Admissions | 45,000 |
| Average Length of Stay | 5.155 days |
| Bed Utilization Rate | 34.94% |
| Occupancy Rate | 25.36% |
| Department Efficiency Score | 90.13 |
| Readmission Rate | Not available |

**KPI note:** Occupancy rate, bed utilization rate, and department efficiency score are currently displayed as fixed values in the Tableau workbook. Their definitions and calculations require validation before they can be treated as dynamic measures. Readmission rate has not been established in the current KPI summary.

## 6. Dataset Overview

The project uses hospital datasets covering:

- Patient information
- Admissions and discharges
- Beds and wards
- Departments and doctors
- Billing and billing details
- Diagnostic tests and patient diagnostics
- Prescriptions
- Patient insurance and insurance providers
- Staff assignments

Prepared analytical datasets are organized around hospital overview, patient flow, department analytics, resource utilization, and KPI summaries.

## 7. Project Structure

```text
Hospital-Performance-Intelligence-System/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
├── notebooks/
├── Milestone-1/
├── Milestone-2/
├── Milestone-3/
├── Milestone-4/
├── Final-Presentation/
└── README.md
```

The structure above describes the main project organization. Individual files may vary according to the current repository contents.

## 8. How to Explore the Project

1. Open the published Tableau Public workbook.
2. Start from the Home dashboard.
3. Select one of the four dashboard navigation buttons.
4. Explore the KPI cards, charts, tooltips, and available filters.
5. Use the supporting project documentation to understand the data and KPI limitations.

## 9. Published Dashboard

**Tableau Public:** [Hospital Performance Intelligence System](https://public.tableau.com/app/profile/smitha.s1071/viz/Hospital_Performance_Intelligence_System/Home)

## 10. Limitations

- Readmission rate is not available in the current KPI summary.
- Selected KPI values are fixed values rather than dynamically calculated measures.
- Resource availability calculations require further validation.
- The accuracy of analytical results depends on the quality and definitions of the underlying datasets.

## 11. Future Enhancements

- Implement dynamic and validated KPI calculations.
- Add readmission analysis using appropriate patient admission history.
- Validate resource availability using bed-level records.
- Expand interactive filters and cross-dashboard analysis.
- Improve automated data validation and refresh processes.

## 12. Conclusion

The Hospital Performance Intelligence System demonstrates how data preparation, KPI summaries, and interactive visualization can be combined to explore hospital operations and patient analytics. The published dashboard suite provides a unified view of hospital activity, with further KPI and resource validation identified as areas for improvement.
# Milestone 3: Dashboard Integration Report

## 1. Project Information

**Project Title:** Hospital Performance Intelligence System  
**Project Name:** MedTrack_DV  
**Domain:** Hospital Operations and Patient Care Analytics  
**Visualization Tool:** Tableau Public  
**Milestone:** 3 – Dashboard Integration

## 2. Objective

The objective of this milestone is to integrate the hospital analytics dashboards into a unified dashboard suite. The system provides an interactive view of hospital admissions, patient flow, department performance, and resource utilization.

## 3. Dashboard Components

### 3.1 Home Dashboard
Provides an introductory landing page with navigation options to the four main dashboards.

### 3.2 Hospital Overview Dashboard
Displays key performance indicators, including total admissions, average length of stay, bed utilization rate, occupancy rate, and department efficiency score. It also presents monthly admission and discharge trends.

### 3.3 Patient Flow Dashboard
Presents patient movement trends, monthly discharges, and the distribution of elective and emergency admissions.

### 3.4 Department Analytics Dashboard
Provides department-level analysis of admissions and billing to support comparisons of hospital activity and financial performance.

### 3.5 Resource Utilization Dashboard
Displays resource utilization analysis and department-wise resource availability.

## 4. Navigation and Integration

The Home dashboard provides navigation buttons for the four main dashboards. The navigation buttons were tested on the published Tableau Public workbook and were confirmed to open their respective dashboards.

The dashboard suite is organized to help users move between hospital-wide indicators and more detailed operational views.

## 5. Key Performance Indicators

| KPI | Reported Value |
|---|---:|
| Total Admissions | 45,000 |
| Average Length of Stay | 5.155 days |
| Bed Utilization Rate | 34.94% |
| Occupancy Rate | 25.36% |
| Department Efficiency Score | 90.13 |
| Readmission Rate | Not available |

The occupancy, bed utilization, and department efficiency values are currently displayed as fixed values in the Tableau workbook. They should be validated against their underlying definitions before being treated as dynamically calculated measures. Readmission rate could not be established from the available KPI summary.

## 6. Testing Status

- Home dashboard is available in the published workbook.
- All four dashboard navigation buttons were tested and confirmed to work online.
- Detailed filter behavior, KPI accuracy, and resource calculation validation require separate checks before final submission.

## 7. Deliverables

- Tableau packaged workbook: `medtrack_dashboard_v1.twbx`
- Dashboard integration report: `dashboard_integration_report.md`
- Tableau dashboard suite published on Tableau Public.

## 8. Conclusion

The project provides a unified interface for exploring hospital operational and patient analytics. The four main dashboards and Home dashboard are available in the published workbook. Additional quality assurance and documentation will be completed as part of Milestone 4.s
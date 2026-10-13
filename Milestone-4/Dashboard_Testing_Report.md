# Dashboard Testing Report

## 1. Project Details

- **Project Title:** Hospital Performance Intelligence System
- **Project Name:** MedTrack_DV
- **Domain:** Hospital Operations and Patient Care Analytics
- **Visualization Tool:** Tableau Public
- **Milestone:** 4 – Dashboard Testing and Quality Assurance

## 2. Testing Objectives

The objective of testing is to assess dashboard navigation, presentation, KPI display, chart readability, filter functionality, and accessibility of the published workbook.

## 3. Dashboard Inventory

| No. | Dashboard | Purpose | Testing Observation |
|---:|---|---|---|
| 1 | Home | Provides access to the main dashboards | Published landing page opens successfully |
| 2 | Hospital Overview | Presents hospital-wide KPIs and admission and discharge trends | Included in the published dashboard suite |
| 3 | Patient Flow | Presents patient movement, discharge trends, and admission types | Navigation tested successfully |
| 4 | Department Analytics | Presents department admissions and billing analysis | Navigation tested successfully |
| 5 | Resource Utilization | Presents resource utilization and department-wise availability | Navigation tested successfully |

## 4. Test Cases and Results

| Test ID | Test Case | Current Result | Status |
|---|---|---|---|
| TC01 | Open the published workbook | Home dashboard is accessible online | Passed |
| TC02 | Navigate to Hospital Overview | Dashboard is included in the published workbook | Navigation verification recorded |
| TC03 | Navigate to Patient Flow | Correct dashboard opens | Passed |
| TC04 | Navigate to Department Analytics | Correct dashboard opens | Passed |
| TC05 | Navigate to Resource Utilization | Correct dashboard opens | Passed |
| TC06 | Inspect KPI values | KPI values are displayed | Calculation validation required |
| TC07 | Inspect chart labels and titles | Titles and axis labels have been configured | Reviewed |
| TC08 | Inspect chart tooltips | Selected tooltips display relevant fields | Reviewed |
| TC09 | Test dashboard filters | Department filter is available on Resource Utilization | Further behavior testing required |
| TC10 | Validate resource availability | Available Beds figure needs investigation | Validation required |
| TC11 | Validate readmission rate | Not available in the current KPI summary | Data limitation |
| TC12 | Verify packaged workbook | Packaged workbook exists locally | Confirmed |

## 5. KPI Results

| KPI | Displayed Value |
|---|---:|
| Total Admissions | 45,000 |
| Average Length of Stay | 5.155 days |
| Bed Utilization Rate | 34.94% |
| Occupancy Rate | 25.36% |
| Department Efficiency Score | 90.13 |
| Readmission Rate | Not available |

The displayed values are recorded for reference. Total admissions and average length of stay should be compared with their source data. Occupancy, bed utilization, and department efficiency are currently displayed as fixed values in Tableau and require formula validation. Readmission rate has not been established from the current KPI summary.

## 6. Observations and Limitations

1. The Home dashboard provides navigation to the four principal dashboards.
2. The published workbook is accessible through Tableau Public.
3. Selected chart titles, axis labels, and tooltips have been configured.
4. The department filter is available on the Resource Utilization dashboard.
5. Some KPI values are fixed values rather than dynamically calculated measures.
6. The Available Beds figure requires verification against the source data and correct aggregation method.
7. Readmission rate requires suitable patient-level admission history and a defined readmission period.

## 7. Recommended Validation

- Compare total admissions with the admission dataset.
- Recalculate average length of stay from admission and discharge dates.
- Verify the definitions and formulas used for occupancy and bed utilization.
- Confirm the department efficiency score calculation.
- Apply filters and verify that displayed charts respond correctly.
- Check resource availability against distinct bed records and their status.
- Record screenshots or other evidence for completed tests.
- Correct any discrepancies before final submission.

## 8. Conclusion

The Hospital Performance Intelligence System provides a published suite of hospital analytics dashboards. The Home page and navigation to the main dashboards have been tested, and the workbook is accessible online.

This report records the observed functionality, displayed KPI values, and outstanding validation requirements. Final testing approval should be provided after the remaining calculation and filter checks have been completed.
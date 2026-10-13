# Milestone 4: Quality Assurance Checklist

## 1. Project Information

- **Project Title:** Hospital Performance Intelligence System
- **Project Name:** MedTrack_DV
- **Domain:** Hospital Operations and Patient Care Analytics
- **Visualization Platform:** Tableau Public
- **Milestone:** 4 – Quality Assurance and Testing

## 2. Dashboard Functionality and Quality Assurance

| No. | Test Item | Status | Result |
|---:|---|---|---|
| 1 | Home dashboard displays the project title and introduction | Verified | Project landing page is visible on Tableau Public |
| 2 | Hospital Overview dashboard navigation | Verified | Dashboard is included in the published workbook |
| 3 | Patient Flow dashboard navigation | Verified | Navigation button opens the corresponding dashboard |
| 4 | Department Analytics dashboard navigation | Verified | Navigation button opens the corresponding dashboard |
| 5 | Resource Utilization dashboard navigation | Verified | Navigation button opens the corresponding dashboard |
| 6 | Navigation buttons lead to the correct dashboards | Verified | All four navigation buttons tested successfully |
| 7 | KPI display and source-data consistency | Review documented | KPI values are recorded; calculation definitions require validation |
| 8 | Dashboard filters | Implemented | Department filter is available on the Resource Utilization dashboard |
| 9 | Chart titles and axis labels | Reviewed | Chart titles and axis labels have been configured |
| 10 | Chart tooltips | Reviewed | Selected chart tooltips display relevant information |
| 11 | Dashboard layout and readability | Reviewed | Dashboard layouts have been visually inspected |
| 12 | Resource availability calculations | Requires validation | Available Beds figure requires comparison with source data |
| 13 | Published workbook accessibility | Verified | Published Home dashboard opens successfully on Tableau Public |
| 14 | Packaged workbook availability | Verified | Tableau packaged workbook is stored in the project folder |

## 3. Key Performance Indicator Validation

The following KPI values are displayed in the dashboard suite.

| KPI | Displayed Value | Validation Notes |
|---|---:|---|
| Total Admissions | 45,000 | Compare against the admission dataset |
| Average Length of Stay | 5.155 days | Compare against the source discharge and admission records |
| Bed Utilization Rate | 34.94% | Confirm the calculation formula and denominator |
| Occupancy Rate | 25.36% | Confirm the calculation formula and denominator |
| Department Efficiency Score | 90.13 | Confirm the score definition and calculation method |
| Readmission Rate | Not available | Not established in the current KPI summary |

**Important:** The occupancy rate, bed utilization rate, and department efficiency score are currently displayed as fixed values in the Tableau workbook. They should not be described as dynamically calculated KPIs until their formulas are implemented and validated.

## 4. Data Quality and Resource Validation

The project uses hospital datasets covering admissions, patients, billing, departments, wards, beds, diagnostics, prescriptions, and insurance.

The final validation process includes:

- Checking dataset fields and data types.
- Comparing dashboard totals with source datasets.
- Checking for missing or invalid values.
- Verifying that resource availability measures use the correct units and aggregation.
- Confirming that displayed KPI values correspond to their documented definitions.
- Recording limitations where the available dataset does not support a calculation.

The displayed Available Beds value requires further inspection because it may represent an aggregated resource count rather than the number of distinct available beds.

## 5. Dashboard Testing Procedure

1. Open the published Tableau Public workbook.
2. Navigate to each dashboard using the Home page.
3. Confirm that the correct dashboard opens from each navigation button.
4. Inspect KPI cards, chart titles, axis labels, and tooltips.
5. Apply available filters and inspect the resulting charts.
6. Compare displayed KPI values with the source datasets and KPI summary.
7. Validate resource availability calculations and aggregation methods.
8. Record test outcomes and resolve any discrepancies.
9. Save the final packaged workbook and retain screenshots as testing evidence.

## 6. Testing Summary

The Home dashboard and all four navigation buttons have been tested successfully on the published Tableau Public workbook. The dashboard suite includes hospital overview, patient flow, department analytics, and resource utilization views.

Chart titles, axis labels, and selected tooltips have been configured. The workbook is available online and a packaged workbook is maintained locally.

KPI calculation validation, detailed filter testing, and resource availability verification remain important quality assurance activities. Readmission rate is not available in the current KPI summary.

## 7. Known Limitations

- Readmission rate has not been established from the current KPI summary.
- Some KPI values are fixed values rather than dynamically calculated Tableau measures.
- Resource availability figures require confirmation against the underlying data.
- Final KPI accuracy should be confirmed before the dashboard is used for operational decision-making.

## 8. Conclusion

The Hospital Performance Intelligence System provides a unified Tableau interface for exploring hospital operations and patient analytics. The published dashboard suite includes a Home page and four main dashboards with working navigation.

This QA checklist documents the implemented functionality, verified navigation, available KPI values, and remaining validation requirements. Final quality assurance approval should be recorded after all outstanding calculations and functionality checks have been completed.
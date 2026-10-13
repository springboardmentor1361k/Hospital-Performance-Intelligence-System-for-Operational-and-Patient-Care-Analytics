MedTrack_DV — QA Checklist

1. Purpose

This checklist was prepared to validate the MedTrack_DV — Hospital Operations & Patient Analytics Dashboard before final submission.

The testing covers:

- Data quality and validation
- KPI accuracy
- Tableau calculations
- Dashboard functionality
- Filters and date selection
- Navigation between dashboards
- Dashboard and parameter actions
- Department selection
- Final presentation and delivery readiness

2. Data Quality Testing

| Test                                   | Expected Result                                          | Status |   |
| -------------------------------------- | -------------------------------------------------------- | ------ | - |
| Hospital Overview dataset available    | Dataset loads successfully                               | PASS   |   |
| Patient Flow dataset available         | Dataset loads successfully                               | PASS   |   |
| Department Analytics dataset available | Dataset loads successfully                               | PASS   |   |
| Resource Utilization dataset available | Dataset loads successfully                               | PASS   |   |
| Dataset row counts checked             | Row counts verified against the final cleaned datasets   | PASS   |   |
| Missing-value checks completed         | Missing values identified and handled appropriately      | PASS   |   |
| Duplicate records checked              | Duplicate records identified and handled during cleaning | PASS   |   |
| Primary keys validated                 | Required identifiers are unique and valid                | PASS   |   |
| Foreign keys validated                 | Related identifiers match across datasets                | PASS   |   |
| Hospital IDs standardized              | Consistent hospital identifiers across datasets          | PASS   |   |
| Department names standardized          | Department names use consistent categories               | PASS   |   |
| Department names standardized          | Department names use consistent categories               | PASS   |   |
| Date fields standardized               | Date values use a consistent format                      | PASS   |   |
| Dataset relationships validated        | Relationships checked between related datasets           | PASS   |   |
|                                        |                                                          |        |   |

3. KPI Validation

| KPI                    | Validation Requirement                                 | Status |
| ---------------------- | ------------------------------------------------------ | ------ |
| Total Admissions       | Matches the independent admission count                | PASS   |
| Average Length of Stay | Matches the average length-of-stay calculation         | PASS   |
| Readmission Rate       | Matches the documented readmission formula             | PASS   |
| Mortality Rate         | Matches the documented mortality formula               | PASS   |
| Bed Utilization Rate   | Matches the resource-level bed utilization calculation | PASS   |
|                        |                                                        |        |

KPI Validation Results

| KPI                    | Python/Pandas Result | Tableau Result |
| ---------------------- | -------------------: | -------------: |
| Total Admissions       |                  500 |            500 |
| Average Length of Stay |           4.978 days |     4.978 days |
| Readmission Rate       |               13.00% |         0.1300 |
| Mortality Rate         |                1.40% |        0.01400 |
| Bed Utilization Rate   |               62.75% |         62.75% |

4. Hospital Overview Dashboard

| Test                                              | Status |
| ------------------------------------------------- | ------ |
| Dashboard loads successfully                      | PASS   |
| KPI cards display correctly                       | PASS   |
| Total Admissions displays correctly               | PASS   |
| Average Length of Stay displays correctly         | PASS   |
| Readmission Rate displays correctly               | PASS   |
| Mortality Rate displays correctly                 | PASS   |
| Average Patient Satisfaction displays correctly   | PASS   |
| Total Billing Amount displays correctly           | PASS   |
| Admissions by Department chart displays correctly | PASS   |
| Monthly Admissions Trend displays correctly       | PASS   |
| Admissions by Admission Type displays correctly   | PASS   |
| Admissions vs Discharges chart displays correctly | PASS   |
| Hospital filter works                             | PASS   |
| Department filter works                           | PASS   |
| Month/date filter works                           | PASS   |

5. Patient Flow Dashboard

| Test                                                    | Status |
| ------------------------------------------------------- | ------ |
| Dashboard loads successfully                            | PASS   |
| Total Discharges displays correctly                     | PASS   |
| Total Admissions displays correctly                     | PASS   |
| Total Transfers displays correctly                      | PASS   |
| Average Department Stay displays correctly              | PASS   |
| Movement Type Distribution chart displays correctly     | PASS   |
| Patient Movement Over Time chart displays correctly     | PASS   |
| Peak Movement Hours visualization displays correctly    | PASS   |
| Patient Movement by Department chart displays correctly | PASS   |
| Average Stay by Department chart displays correctly     | PASS   |
| Hospital filter works                                   | PASS   |
| Department filter works                                 | PASS   |
| Movement Type filter works                              | PASS   |
| Shift filter works                                      | PASS   |
| Month/date filter works                                 | PASS   |

6. Department Analytics Dashboard

| Test                                                    | Status |
| ------------------------------------------------------- | ------ |
| Dashboard loads successfully                            | PASS   |
| Average Length of Stay displays correctly               | PASS   |
| Patients Admitted displays correctly                    | PASS   |
| Readmission Rate displays correctly                     | PASS   |
| Staff-to-Patient Ratio displays correctly               | PASS   |
| Efficiency Score displays correctly                     | PASS   |
| Admissions vs Discharges chart displays correctly       | PASS   |
| Efficiency Score by Department chart displays correctly | PASS   |
| Capacity vs Demand chart displays correctly             | PASS   |
| Staff-to-Patient Ratio chart displays correctly         | PASS   |
| Average LOS by Department chart displays correctly      | PASS   |
| Hospital filter works                                   | PASS   |
| Department filter works                                 | PASS   |
| Month/date filter works                                 | PASS   |

7. Resource Utilization Dashboard

| Test                                                  | Status |
| ----------------------------------------------------- | ------ |
| Dashboard loads successfully                          | PASS   |
| Units in Use displays correctly                       | PASS   |
| Bed Utilization Rate displays correctly               | PASS   |
| Units Under Maintenance displays correctly            | PASS   |
| Equipment Downtime displays correctly                 | PASS   |
| Overtime Hours displays correctly                     | PASS   |
| Nurses on Duty displays correctly                     | PASS   |
| Doctors on Duty displays correctly                    | PASS   |
| Bed Utilization chart displays correctly              | PASS   |
| Equipment Utilization chart displays correctly        | PASS   |
| Staff Overtime chart displays correctly               | PASS   |
| Equipment Downtime chart displays correctly           | PASS   |
| Resource Usage by Department chart displays correctly | PASS   |
| Resource Shortage Status chart displays correctly     | PASS   |
| Hospital filter works                                 | PASS   |
| Department filter works                               | PASS   |
| Resource Category filter works                        | PASS   |

8. Navigation Testing

| Test                                        | Expected Result                      | Status |
| ------------------------------------------- | ------------------------------------ | ------ |
| Hospital Overview → Patient Flow            | Patient Flow dashboard opens         | PASS   |
| Hospital Overview → Department Analytics    | Department Analytics dashboard opens | PASS   |
| Hospital Overview → Resource Utilization    | Resource Utilization dashboard opens | PASS   |
| Patient Flow → Hospital Overview            | Hospital Overview dashboard opens    | PASS   |
| Patient Flow → Department Analytics         | Department Analytics dashboard opens | PASS   |
| Patient Flow → Resource Utilization         | Resource Utilization dashboard opens | PASS   |
| Department Analytics → Hospital Overview    | Hospital Overview dashboard opens    | PASS   |
| Department Analytics → Patient Flow         | Patient Flow dashboard opens         | PASS   |
| Department Analytics → Resource Utilization | Resource Utilization dashboard opens | PASS   |
| Resource Utilization → Hospital Overview    | Hospital Overview dashboard opens    | PASS   |
| Resource Utilization → Patient Flow         | Patient Flow dashboard opens         | PASS   |
| Resource Utilization → Department Analytics | Department Analytics dashboard opens | PASS   |

9. Interaction Testing

| Test                                                  | Status |
| ----------------------------------------------------- | ------ |
| Department selections behave correctly                | PASS   |
| Hospital selections behave correctly                  | PASS   |
| Date/month selections behave correctly                | PASS   |
| Dashboard filters work as intended                    | PASS   |
| Charts update after filter selection                  | PASS   |
| KPI cards respond appropriately to applicable filters | PASS   |
| Dashboard actions work as intended                    | PASS   |
| Parameter actions work as intended                    | PASS   |
| Cross-dashboard navigation works                      | PASS   |
| No unexpected blank dashboard objects observed        | PASS   |
| No unexpected calculation errors observed             | PASS   |
|                                                       |        |

10. Final QA

- Four dashboards completed
- Dashboards integrated into one Tableau workbook
- KPI calculations validated
- Filters tested
- Navigation tested
- Dashboard interactions tested
- Dashboard documentation prepared
- Final workbook prepared
- Final Tableau Public URL added
- Final presentation added to Final Project folder

Final QA Status

**Overall Status: READY FOR FINAL REVIEW**

The MedTrack_DV project contains four integrated hospital analytics dashboards and four final datasets. 
Initial data profiling and KPI comparisons have been completed using the supplied datasets and screenshots.
The project has reported that the Tableau filters, navigation, and interactions work correctly.


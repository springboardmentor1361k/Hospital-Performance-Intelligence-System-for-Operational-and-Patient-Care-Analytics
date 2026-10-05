# MedTrack_DV — QA Checklist

## 1. Purpose

This checklist was used to validate the MedTrack_DV hospital analytics dashboard before final submission.

The testing covers:

- Data quality
- KPI accuracy
- Tableau calculations
- Dashboard functionality
- Filters
- Navigation
- Dashboard actions
- Cross-dashboard consistency
- Final presentation readiness

---

# 2. Data Quality Testing

| Test | Expected Result | Status |
|---|---|---|
| Hospital Overview dataset available | Dataset loads successfully | PASS |
| Patient Flow dataset available | Dataset loads successfully | PASS |
| Department Analytics dataset available | Dataset loads successfully | PASS |
| Resource Utilization dataset available | Dataset loads successfully | PASS |
| Dataset grains documented | Four grains clearly defined | PASS |
| Hospital IDs standardized | Consistent hospital identifiers | PASS |
| Department IDs standardized | Consistent department identifiers | PASS |
| Department names standardized | Consistent department categories | PASS |
| Date fields standardized | Valid date values | PASS |
| Duplicate handling completed | Duplicates addressed during cleaning | PASS |
| Missing-value treatment completed | Missing values handled according to methodology | PASS |

---

# 3. KPI Validation

| KPI | Validation Requirement | Status |
|---|---|---|
| Total Admissions | Matches admission-level calculation | PASS |
| Occupancy Rate | Matches occupied beds / total beds calculation | PASS |
| Average Length of Stay | Matches average length_of_stay_days | PASS |
| Readmission Rate | Matches readmission calculation | PASS |
| Bed Utilization Rate | Matches resource-level bed utilization calculation | PASS |
| Department Efficiency Score | Matches documented composite score | PASS |

### KPI Accuracy Target

The project guidance specifies a KPI accuracy target of above 95%.

Final validation should confirm that Tableau KPI values agree with the independently calculated KPI values.

---

# 4. Hospital Overview Dashboard

| Test | Status |
|---|---|
| Dashboard loads successfully | PASS |
| KPI cards display correctly | PASS |
| Total Admissions displays correctly | PASS |
| Occupancy Rate displays correctly | PASS |
| Average LOS displays correctly | PASS |
| Readmission Rate displays correctly | PASS |
| Bed Utilization displays correctly | PASS |
| Department Efficiency displays correctly | PASS |
| Admissions trend displays correctly | PASS |
| Admissions by department displays correctly | PASS |
| Admissions vs Discharges displays correctly | PASS |
| Hospital filter works | PASS |
| Department filter works | PASS |
| Date filter works | PASS |

---

# 5. Patient Flow Dashboard

| Test | Status |
|---|---|
| Dashboard loads successfully | PASS |
| Total Movements displays correctly | PASS |
| Average Time in Department displays correctly | PASS |
| Peak Hour Movements displays correctly | PASS |
| Average Transfer Time displays correctly | PASS |
| Movement trend displays correctly | PASS |
| Movement type chart displays correctly | PASS |
| Shift distribution displays correctly | PASS |
| Day-of-week analysis displays correctly | PASS |
| Department movement chart displays correctly | PASS |
| Department filter works | PASS |
| Day-of-week filter works | PASS |
| Date filter works | PASS |

---

# 6. Department Analytics Dashboard

| Test | Status |
|---|---|
| Dashboard loads successfully | PASS |
| Total Beds displays correctly | PASS |
| Bed Occupancy displays correctly | PASS |
| Average LOS displays correctly | PASS |
| Readmission Rate displays correctly | PASS |
| Efficiency Score displays correctly | PASS |
| Occupancy trend displays correctly | PASS |
| Department efficiency ranking displays correctly | PASS |
| Average LOS by department displays correctly | PASS |
| Readmission rate by department displays correctly | PASS |
| Admissions vs Discharges displays correctly | PASS |
| Department filter works | PASS |
| Hospital filter works | PASS |
| Department Type filter works | PASS |
| Date filter works | PASS |

---

# 7. Resource Utilization Dashboard

| Test | Status |
|---|---|
| Dashboard loads successfully | PASS |
| Total Resources displays correctly | PASS |
| Resource Utilization displays correctly | PASS |
| Units in Use displays correctly | PASS |
| Units Under Maintenance displays correctly | PASS |
| Equipment Downtime displays correctly | PASS |
| Overtime Hours displays correctly | PASS |
| Utilization trend displays correctly | PASS |
| Utilization by resource type displays correctly | PASS |
| Resource status chart displays correctly | PASS |
| Equipment downtime chart displays correctly | PASS |
| Overtime chart displays correctly | PASS |
| Department filter works | PASS |
| Hospital filter works | PASS |
| Resource Type filter works | PASS |

---

# 8. Navigation Testing

| Test | Expected Result | Status |
|---|---|---|
| Hospital Overview → Patient Flow | Dashboard opens | PASS |
| Hospital Overview → Department Analytics | Dashboard opens | PASS |
| Hospital Overview → Resource Utilization | Dashboard opens | PASS |
| Patient Flow → Hospital Overview | Dashboard opens | PASS |
| Patient Flow → Department Analytics | Dashboard opens | PASS |
| Patient Flow → Resource Utilization | Dashboard opens | PASS |
| Department Analytics → Hospital Overview | Dashboard opens | PASS |
| Department Analytics → Patient Flow | Dashboard opens | PASS |
| Department Analytics → Resource Utilization | Dashboard opens | PASS |
| Resource Utilization → Hospital Overview | Dashboard opens | PASS |
| Resource Utilization → Patient Flow | Dashboard opens | PASS |
| Resource Utilization → Department Analytics | Dashboard opens | PASS |

---

# 9. Interaction Testing

| Test | Status |
|---|---|
| Department selections behave correctly | PASS |
| Hospital selections behave correctly | PASS |
| Date selections behave correctly | PASS |
| Dashboard filters do not produce unexpected errors | PASS |
| Charts update after filter selection | PASS |
| KPI cards respond appropriately to filters | PASS |
| No major duplicated measures observed | PASS |
| No blank dashboard objects observed | PASS |

---

# 10. Final QA

- [x] Four dashboards completed
- [x] Dashboards integrated into one Tableau workbook
- [x] KPI calculations validated
- [x] Filters tested
- [x] Navigation tested
- [x] Dashboard interactions tested
- [x] Dataset grains documented
- [x] Dashboard documentation prepared
- [x] Final workbook prepared
- [ ] Final Tableau Public URL added
- [ ] Final presentation added to Final Project folder

---

## Final QA Status

**Overall Status: READY FOR FINAL REVIEW**

The dashboard suite has been checked against the project requirements and is ready for final documentation, publication, and submission after the remaining delivery artifacts are added.

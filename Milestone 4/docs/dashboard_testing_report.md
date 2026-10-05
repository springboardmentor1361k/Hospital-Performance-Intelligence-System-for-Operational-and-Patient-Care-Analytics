# MedTrack_DV — Dashboard Testing Report

## 1. Introduction

This report documents the testing and validation performed on the MedTrack_DV Hospital Operations & Patient Analytics Dashboard.

The objective of testing was to verify that:

- The four dashboards function correctly.
- KPI calculations are consistent with the documented formulas.
- Filters work correctly.
- Dashboard navigation works correctly.
- Dashboard interactions behave as expected.
- The dashboards present meaningful operational information.
- The final Tableau workbook functions as an integrated dashboard suite.

---

# 2. Dashboards Tested

The following dashboards were tested:

1. Hospital Overview
2. Patient Flow
3. Department Analytics
4. Resource Utilization

All four dashboards are contained within the MedTrack_DV Tableau workbook.

---

# 3. Data Validation

The dashboard testing process considered the four analytical datasets:

| Dataset | Grain |
|---|---|
| Hospital Overview | One row per admission |
| Patient Flow | One row per movement event |
| Department Analytics | One hospital + department + day |
| Resource Utilization | One hospital + department + date + resource type |

The different dataset grains were considered during dashboard development to avoid unnecessary duplication of measures.

---

# 4. KPI Testing

The six mandatory KPIs were tested against their documented definitions.

### Total Admissions

```text
COUNTD(admission_id)

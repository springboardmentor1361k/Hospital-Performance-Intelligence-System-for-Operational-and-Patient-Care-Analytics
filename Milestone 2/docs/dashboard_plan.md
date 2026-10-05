# Dashboard Plan

## Evidence and Status

The README identifies a planned four-dashboard suite and says filters, navigation, hospital/department comparisons, dashboard actions, and simple wireframes were planned. The existing [six-page storyboard PDF](../reports/dashboard_storyboard.pdf) is retained. Its page text was not extractable with the available runtime tools during this audit, and no Tableau workbook or dashboard screenshots are present in the repository. The details below distinguish confirmed dataset/KPI mappings from planning specifications that remain unavailable; proposed chart types and control behavior are not presented as approved design.

**Shared data-model rule:** Do not physically join all four analytical datasets indiscriminately. Their grains differ; a join can multiply rows and duplicate measures. Use Tableau relationships or separate dashboard-level data sources, and aggregate within the source grain before combining results.

**Shared interaction status:** README-level evidence says filters, navigation, dashboard actions, and hospital/department comparisons were planned. Exact filter fields, navigation pattern, action definitions, and comparison behavior are not documented and must be confirmed against the storyboard before implementation.

## 1. Hospital Overview

| Item | Plan/evidence |
|---|---|
| Purpose | Present an overview of hospital admissions and operational performance, based on the dashboard name and project scope. |
| Intended users | Not named in repository documentation. |
| Key KPIs | Total Admissions, Occupancy Rate, Average Length of Stay, and Readmission Rate are available from the existing KPI set; whether all appear on this dashboard is not recorded. |
| Charts/visualizations | Exact visualizations are not specified in inspectable repository text; confirm from the storyboard. |
| Filters | Filters are mentioned as planned in README; fields and controls are unspecified. |
| Navigation | Part of the planned four-dashboard suite; exact navigation is unspecified. |
| Dashboard actions | Actions are mentioned as planned in README; trigger and behavior are unspecified. |
| Comparisons | Hospital comparison is mentioned as planned; dimensions and comparison method are unspecified. |
| Primary dataset(s) | Hospital Overview; Department Analytics for the existing occupancy KPI. |

## 2. Patient Flow

| Item | Plan/evidence |
|---|---|
| Purpose | Explore patient movement events and their recorded time/department context. |
| Intended users | Not named in repository documentation. |
| Key KPIs | No mandatory KPI is defined specifically from Patient Flow in the existing six-KPI calculation. The dataset includes event, duration, shift, and time fields. |
| Charts/visualizations | Exact visualizations are unspecified; confirm from the storyboard. |
| Filters | Filters are mentioned as planned; fields and controls are unspecified. |
| Navigation | Part of the planned four-dashboard suite; exact navigation is unspecified. |
| Dashboard actions | Actions are mentioned as planned; trigger and behavior are unspecified. |
| Comparisons | Hospital/department comparisons are mentioned generally in README; Patient Flow-specific comparison behavior is unspecified. |
| Primary dataset(s) | Patient Flow. |

## 3. Department Analytics

| Item | Plan/evidence |
|---|---|
| Purpose | Present daily operational measures at hospital + department + day grain. |
| Intended users | Not named in repository documentation. |
| Key KPIs | Occupancy Rate and Department Efficiency Score use Department Analytics in the current KPI logic. The stored dataset also includes daily operational measures. |
| Charts/visualizations | Exact visualizations are unspecified; confirm from the storyboard. |
| Filters | Filters are mentioned as planned; fields and controls are unspecified. |
| Navigation | Part of the planned four-dashboard suite; exact navigation is unspecified. |
| Dashboard actions | Actions are mentioned as planned; trigger and behavior are unspecified. |
| Comparisons | Department and hospital comparisons are mentioned as planned; exact dimensions and method are unspecified. |
| Primary dataset(s) | Department Analytics. |

## 4. Resource Utilization

| Item | Plan/evidence |
|---|---|
| Purpose | Present resource availability, use, capacity, and maintenance measures. |
| Intended users | Not named in repository documentation. |
| Key KPIs | Bed Utilization Rate uses Resource Utilization filtered to Bed. Other measures are present in the dataset but are not among the six mandatory KPIs. |
| Charts/visualizations | Exact visualizations are unspecified; confirm from the storyboard. |
| Filters | Filters are mentioned as planned; fields and controls are unspecified. |
| Navigation | Part of the planned four-dashboard suite; exact navigation is unspecified. |
| Dashboard actions | Actions are mentioned as planned; trigger and behavior are unspecified. |
| Comparisons | Hospital/department comparisons are mentioned generally; Resource Utilization-specific behavior is unspecified. |
| Primary dataset(s) | Resource Utilization. |

## Before Tableau Implementation

Confirm exact visualizations, filter fields, navigation, actions, comparison behavior, and intended audiences by reviewing the storyboard pages. Keep source grains separate or related, and verify that any cross-source KPI calculation is not affected by row multiplication. No Tableau dashboard completion is asserted by this plan.

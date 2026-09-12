# Milestone 2 Report

## Hospital Performance Intelligence System

---

## 1. Introduction

Milestone 2 focuses on preparing hospital data for analytical visualization and defining the key performance indicators required for the Hospital Performance Intelligence System.

The work includes KPI formulation, KPI validation, preparation of analytical datasets, Tableau data modelling and storyboard planning.

---

## 2. Objectives

The main objectives of Milestone 2 are:

- Define important hospital performance indicators.
- Formulate suitable KPI calculation methods.
- Validate the calculated KPI values.
- Prepare datasets for Tableau visualization.
- Define the Tableau data model.
- Design the dashboard storyboard.
- Identify limitations and future improvements.

---

## 3. Prepared Analytical Datasets

Four analytical datasets were prepared from the cleaned Hospital HMIS data.

| Dataset | Grain | Purpose |
|---|---|---|
| Hospital Overview | One row per hospital admission | Overall hospital performance analysis |
| Patient Flow | One row per patient movement event | Admission and discharge analysis |
| Department Analytics | One hospital, department and day | Department performance comparison |
| Resource Utilization | One hospital, department, day and resource type | Bed and resource utilization analysis |

The processed datasets are stored in the `data/processed` directory.

---

## 4. Key Performance Indicators

The following KPIs were selected for the project:

1. Total Admissions
2. Occupancy Rate
3. Average Length of Stay
4. Readmission Rate
5. Bed Utilization Rate
6. Department Efficiency Score

These indicators were selected to represent hospital workload, patient stay, bed usage, patient outcomes and departmental performance.

---

## 5. KPI Definitions and Formulas

### 5.1 Total Admissions

Total Admissions represents the total number of hospital admission records.

```text
Total Admissions = Count of unique admission IDs
5.2 Average Length of Stay

Average Length of Stay represents the average number of days patients stayed in the hospital.

Average Length of Stay =
Total Length of Stay Days / Total Admissions
5.3 Occupancy Rate

Occupancy Rate measures the proportion of available bed capacity used during the observation period.

Occupancy Rate =
Total Patient-Days / (Total Beds × Number of Days) × 100
5.4 Readmission Rate

Readmission Rate measures the percentage of patients who return to the hospital after a previous admission.

Readmission Rate =
Number of Readmitted Patients / Total Discharged Patients × 100

The Readmission Rate could not be calculated because the required approved readmission dataset has not yet been integrated.

5.5 Bed Utilization Rate

Bed Utilization Rate measures the percentage of registered beds that were used.

Bed Utilization Rate =
Number of Used Beds / Total Registered Beds × 100
5.6 Department Efficiency Score

The Department Efficiency Score is a normalized score used to compare department performance.

The score considers admissions per bed and average length of stay. Higher admissions per bed and lower average length of stay contribute positively to the score.

Department Efficiency Score =
60% × Normalized Admissions per Bed
+
40% × Inverse Normalized Average Length of Stay

The score is represented on a scale of 0 to 100.

6. KPI Calculation Results

The KPI calculation script was executed using the prepared Hospital Overview, Ward and Bed datasets.

KPI

	

Calculated Result




Total Admissions

	

45,000




Average Length of Stay

	

5.16 days




Occupancy Rate

	

25.36%




Readmission Rate

	

Not available




Bed Utilization Rate

	

34.94%




Average Department Efficiency Score

	

90.13/100

Additional calculated values include:

Total available beds: 415

Total registered beds: 415

Used beds: 145

Total patient-days: 231,975

Number of days covered: 2,204

7. KPI Validation

The calculated KPIs were checked using the following validation methods:

Admission IDs were checked for uniqueness.

Length of stay values were checked for invalid or negative values.

Date fields were checked for valid admission and discharge dates.

Foreign-key relationships were checked between admission, patient, department, ward, bed and disease tables.

Bed counts were checked against the cleaned bed and ward datasets.

Department-level calculations were compared with the generated department KPI summary.

The KPI output was saved in the processed data directory.

The validation confirmed that the main admission-level data was suitable for preliminary KPI calculation.

The Readmission Rate remains unavailable until the approved patient readmission dataset is collected and integrated.

8. Tableau Data Model

The Tableau model separates the datasets according to their analytical grain.

The Hospital Overview dataset contains admission-level records. The Patient Flow dataset contains multiple movement events for an admission. The Department Analytics dataset contains department-level daily summaries, while the Resource Utilization dataset contains department-level daily resource information.

This separation helps reduce duplication and prevents incorrect aggregation during visualization.

The detailed Tableau data model is documented in:

Milestone-2/documentation/tableau_data_model.md
9. Tableau Storyboard

The planned Tableau storyboard contains four major story points:

Hospital Overview

Patient Flow Analysis

Department Analytics

Resource Utilization

The Hospital Overview page will display the major KPIs and admission trends.

The Patient Flow page will show admission and discharge patterns.

The Department Analytics page will compare departmental workload, length of stay and efficiency.

The Resource Utilization page will show bed availability, used beds, occupancy and utilization.

The detailed storyboard is documented in:

Milestone-2/documentation/tableau_storyboard.md
10. Dashboard Design Plan

The planned dashboard will include:

KPI cards

Line charts for trends

Bar charts for department comparisons

Admission and discharge comparisons

Bed utilization visuals

Interactive filters

Department and ward-level analysis

Recommended filters include:

Admission Date

Discharge Date

Department Name

Department Type

Ward Name

Admission Type

Admission Status

Gender

Disease Category

Payment Status

11. Limitations

The current Milestone 2 implementation has the following limitations:

The approved external datasets have not yet been fully integrated.

Readmission Rate is currently unavailable.

The current Bed Utilization Rate is based on the number of used beds compared with registered beds.

The Department Efficiency Score is a preliminary normalized score.

The Tableau dashboard implementation is planned based on the prepared data model and storyboard.

Additional validation will be performed during the final dashboard development phase.

12. Future Work

The following activities will be completed in the next phase:

Collect and integrate the remaining approved datasets.

Calculate and validate Readmission Rate.

Develop the interactive Tableau dashboard.

Implement dashboard filters and actions.

Validate Tableau values against Python outputs.

Improve KPI definitions based on mentor feedback.

Prepare the final project presentation and report.

13. Deliverables Completed

The following Milestone 2 deliverables have been prepared:

KPI calculation script

KPI summary dataset

Department KPI summary dataset

KPI definitions and validation document

Tableau data model document

Tableau storyboard document

Four processed analytical datasets

Milestone 2 report

14. Conclusion

Milestone 2 established the analytical foundation for the Hospital Performance Intelligence System.

The cleaned hospital data was transformed into four analytical datasets, and the required KPIs were formulated and calculated. The Tableau data model and storyboard provide a structured plan for developing the final dashboard.

The current results demonstrate that the prepared data can support hospital admission analysis, patient flow monitoring, department comparison and resource utilization analysis. Further work will focus on integrating the remaining datasets and implementing the interactive Tableau dashboard.
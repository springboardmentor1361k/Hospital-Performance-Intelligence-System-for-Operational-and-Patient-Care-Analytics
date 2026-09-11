# Hospital-Performance-Intelligence-System-for-Operational-and-Patient-Care-Analytics

## MedTrack_DV — Milestone 1

I have successfully completed **Milestone 1 by collecting, profiling, cleaning, validating, and preparing the datasets required for the MedTrack_DV Hospital Operations & Patient Analytics Dashboard**.

### What I completed

* Collected and organized the four required datasets:

  * Hospital Overview
  * Patient Flow
  * Department Analytics
  * Resource Utilization
* Preserved the original datasets in the `data/raw/` folder.
* Performed basic data profiling to check:

  * Dataset shape
  * Missing values
  * Duplicate records
  * Data types and basic data quality
* Cleaned the datasets by:

  * Removing duplicate rows
  * Cleaning text fields
  * Standardizing IDs and categorical values
  * Converting date fields into consistent formats
  * Handling invalid values where required
* Validated the cleaned data for:

  * Remaining duplicates
  * Missing-value levels
  * Valid numerical ranges
  * Relationships between important IDs such as patients and admissions
* Saved the final cleaned datasets in the `data/processed/` folder.
* Created the required documentation and notebook to make the data preparation process reproducible.


This milestone provides the **clean and validated data foundation** that will be used for the next stage of the project: **KPI calculation, analysis, and dashboard development**.

---

## Milestone 2 — KPI Engineering & Dashboard Planning

Milestone 2 focused on transforming the cleaned hospital datasets into a Tableau-ready analytical foundation and planning the dashboard experience.

### Completed Work

- Calculated and validated the six mandatory hospital KPIs:
  - Total Admissions
  - Occupancy Rate
  - Average Length of Stay
  - Readmission Rate
  - Bed Utilization Rate
  - Department Efficiency Score
- Created the reusable `generate_hospital_kpis.py` script for KPI calculation and validation.
- Generated `hospital_final_dataset.xlsx` containing the KPI summary and processed datasets.
- Documented KPI definitions, formulas, source datasets, and calculation logic.
- Designed a dashboard storyboard covering four interconnected dashboards:
  - Hospital Overview
  - Patient Flow
  - Department Analytics
  - Resource Utilization
- Planned dashboard filters, navigation, department/hospital comparisons, and dashboard actions.
- Created simple wireframes to define the layout and visual hierarchy before Tableau development.

### Milestone 2 Outcome

The project now has a validated KPI layer and a structured dashboard blueprint ready for the Tableau development phase. The dashboard design follows the documented dataset grains and avoids unnecessary merging of the four analytical datasets.

---

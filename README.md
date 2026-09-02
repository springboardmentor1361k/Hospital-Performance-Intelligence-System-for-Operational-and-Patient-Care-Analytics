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

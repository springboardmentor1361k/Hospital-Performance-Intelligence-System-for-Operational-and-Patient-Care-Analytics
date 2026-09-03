# Hospital-Performance-Intelligence-System-for-Operational-and-Patient-Care-Analytics

# MedTrack_DV – Milestone 1 & Milestone 2

## Project Overview

**MedTrack_DV** is a Hospital Performance Intelligence System designed to analyze hospital operations, patient flow, department performance, resource utilization, and patient outcomes.

The project uses data preparation, validation, transformation, KPI development, and dashboarding to convert raw healthcare data into meaningful analytical insights for hospital management.

---

# Milestone 1 – Data Collection & Preparation

### Objective

The objective of Milestone 1 was to collect the required hospital healthcare data, understand its structure, identify important analytical fields, and prepare the dataset for further cleaning and analysis.

### Work Performed

**1. Data Collection**

The healthcare dataset was collected from Kaggle and loaded into the project environment using Python. The raw dataset contains patient admission records along with hospital, department, admission, discharge, billing, test-result, and resource-related information.

**2. Data Understanding**

The dataset was examined to understand:

* Number of records and columns
* Data types of each field
* Patient and hospital identifiers
* Admission and discharge information
* Department and admission types
* Patient demographics
* Readmission information
* Hospital resource fields
* Bed and staff-related information

This step helped identify which columns could be used for the project's KPIs and dashboards.

**3. Data Quality Assessment**

Initial data-quality checks were performed to identify:

* Missing values
* Duplicate records
* Incorrect or inconsistent data types
* Invalid date fields
* Inconsistent categorical values
* Important fields required for analysis

Key columns were also verified to ensure that the dataset contained the required information for further processing.

**4. Data Cleaning & Preparation**

The raw data was processed using Python and the data-cleaning notebook. The cleaning process focused on making the dataset consistent and analysis-ready by handling data-quality issues, standardizing fields, and preparing calculated fields required for hospital analytics.

**5. Clean Dataset Creation**

After the cleaning and preparation process, a cleaned CSV dataset was generated. This cleaned dataset became the input for the KPI-development and dashboard-preparation activities in Milestone 2.

### Milestone 1 Output

* Raw healthcare dataset
* Cleaned healthcare dataset
* Data collection Python script
* Data-cleaning Jupyter Notebook

---

# Milestone 2 – KPI Development & Dashboard Preparation

### Objective

The objective of Milestone 2 was to transform the cleaned hospital data into an analytical dataset, calculate the project's required KPIs, and prepare the initial dashboard structure for visualization.

### Work Performed

**1. Cleaned Dataset Validation**

The cleaned dataset generated in Milestone 1 was loaded into Python and reviewed before KPI calculations. Required fields such as admissions, length of stay, readmission status, bed information, department, and waiting time were checked for analytical use.

**2. KPI Development**

Python was used to calculate the project's six core hospital performance KPIs:

* **Total Admissions** – measures the total number of admission records.
* **Occupancy Rate** – measures the proportion of occupied beds relative to total beds.
* **Average Length of Stay (LOS)** – measures the average number of days patients stay in the hospital.
* **Readmission Rate** – measures the percentage of patients identified as readmissions.
* **Bed Utilization Rate** – evaluates how effectively available bed capacity is being utilized.
* **Department Efficiency** – evaluates department-level operational performance using the available departmental performance information.

The KPI calculations were implemented through a Python script so that the results could be reproduced consistently.

**3. Analytical Dataset Preparation**

The processed hospital data and KPI-related fields were prepared for further analysis and visualization. The final analytical dataset was exported into Excel format for use during dashboard development.

**4. Dashboard Planning**

A dashboard storyboard was prepared to define the structure and analytical flow of the final visualization. The dashboard planning considered hospital-level KPIs, patient flow, department performance, and resource utilization.

**5. Tableau Prototype Development**

An initial Tableau prototype was created to test the dashboard structure, KPI presentation, and visualization approach before development of the final integrated dashboard.

### Milestone 2 Output

* Final analytical dataset
* KPI-generation Python script
* Dashboard storyboard
* Tableau prototype

---

# Current Project Status

Milestones 1 and 2 established the foundation of the MedTrack_DV project.

The work completed so far covers the **data collection → data profiling → data cleaning → KPI development → analytical dataset preparation → dashboard planning → Tableau prototyping** stages.

The next stage is to validate the final data model and develop the complete set of interconnected dashboards covering:

1. **Hospital Overview**
2. **Patient Flow**
3. **Department Analytics**
4. **Resource Utilization**

The final dashboards will use the validated data model and project-defined KPIs to provide a consolidated view of hospital operational and patient-care performance.

# Hospital-Performance-Intelligence-System-for-Operational-and-Patient-Care-Analytics

## MedTrack_DV – Complete Project Documentation (Milestone 1 to Milestone 4)

### Project Overview
**MedTrack_DV** is a Hospital Performance Intelligence System designed to analyze hospital operations, patient flow, department performance, resource utilization, and patient outcomes[cite: 4].
The project uses data preparation, validation, transformation, KPI development, and dashboarding to convert raw healthcare data into meaningful analytical insights for hospital management[cite: 4].

---

### Milestone 1 – Data Collection & Preparation
#### Objective
The objective of Milestone 1 was to collect the required hospital healthcare data, understand its structure, identify important analytical fields, and prepare the dataset for further cleaning and analysis[cite: 4].

#### Work Performed
1. **Data Collection:** The healthcare dataset was collected from Kaggle and loaded into the project environment using Python[cite: 4]. The raw dataset contains patient admission records along with hospital, department, admission, discharge, billing, test-result, and resource-related information[cite: 4].
2. **Data Understanding:** The dataset was examined to understand records, columns, data types, patient/hospital identifiers, admission/discharge info, department types, demographics, readmission info, and resource fields to build KPIs[cite: 4].
3. **Data Quality Assessment:** Initial data-quality checks were performed to identify missing values, duplicate records, incorrect data types, invalid date fields, and inconsistent categorical values[cite: 4].
4. **Data Cleaning & Preparation:** The raw data was processed using Python and data-cleaning notebooks to make the dataset consistent and analysis-ready[cite: 4].
5. **Clean Dataset Creation:** After cleaning, a standardized CSV dataset was generated as input for Milestone 2[cite: 4].

#### Milestone 1 Output
* Raw healthcare dataset (`hospital_raw_data.csv`)[cite: 4]
* Cleaned healthcare dataset (`hospital_cleaned.csv`)[cite: 4]
* Data collection Python script (`data_collection.py`)[cite: 4]
* Data-cleaning Jupyter Notebook (`hospital_cleaning.ipynb`)[cite: 4]

---

### Milestone 2 – KPI Development & Dashboard Preparation
#### Objective
The objective of Milestone 2 was to transform the cleaned hospital data into an analytical dataset, calculate the project's required KPIs, and prepare the initial dashboard structure for visualization[cite: 4].

#### Work Performed
1. **Cleaned Dataset Validation:** Verified fields like admissions, length of stay, readmission status, bed info, department, and waiting time before KPI calculations[cite: 4].
2. **KPI Development:** Python was used to calculate core hospital performance metrics[cite: 4]:
   * **Total Admissions:** Measures total admission records[cite: 4].
   * **Occupancy Rate:** Proportion of occupied beds relative to total beds[cite: 4].
   * **Average Length of Stay (LOS):** Average number of days patients stay[cite: 4].
   * **Readmission Rate:** Percentage of patients identified as readmissions[cite: 4].
   * **Bed Utilization Rate:** Evaluates available bed capacity utilization[cite: 4].
   * **Department Efficiency:** Evaluates department-level operational performance[cite: 4].
3. **Analytical Dataset Preparation:** Exported final processed hospital data into Excel format for dashboard development[cite: 4].
4. **Dashboard Planning:** Prepared a dashboard storyboard defining structure, layout grids, and analytical flow[cite: 4].
5. **Tableau Prototype Development:** Created an initial Tableau prototype (`medtrack_prototype.twbx`) to verify visualization approach[cite: 4].

#### Milestone 2 Output
* Final analytical dataset (`hospital_final_dataset.xlsx`)[cite: 4]
* KPI-generation Python script (`generate_hospital_kpis.py`)[cite: 4]
* Dashboard storyboard (`dashboard_storyboard.pdf`)[cite: 4]
* Tableau prototype (`medtrack_prototype.twbx`)[cite: 4]

---

### Milestone 3 – Dashboard Development & Integration
#### Objective
The objective of Milestone 3 was to build and integrate the four core interactive Tableau dashboards using a modern executive dark theme (`#0F172A` background, `#1E293B` cards, Cyan `#00F2FE` and Amber `#F59E0B` accents).

#### Work Performed
1. **Hospital Overview Dashboard:** Built high-level executive KPIs, monthly occupancy trends, and top-level summaries[cite: 5].
2. **Patient Flow Dashboard:** Developed admission vs discharge tracking, average length of stay by department, and peak patient load analytics[cite: 5].
3. **Department Analytics Dashboard:** Created department efficiency comparisons, capacity vs occupancy tree maps, and medical staff distributions[cite: 5].
4. **Resource Utilization Dashboard:** Implemented bed utilization tracking, active clinical staff metrics, equipment utilization grids, and customized branding badge stickers.
5. **Dashboard Integration & Interactivity:** Configured global filters (Hospital, Department, Region, Date Range), parameter actions, and cross-tab navigation controls[cite: 5].

#### Milestone 3 Output
* Integrated Tableau Workbook (`MedTrack_DV.twbx`)[cite: 5]

---

### Milestone 4 – Testing, Validation & Delivery
#### Objective
The objective of Milestone 4 was to validate metrics, test dashboard interactivity, ensure zero calculation errors, and establish professional project documentation for portfolio deployment[cite: 5].

#### Work Performed
1. **Testing & Validation:** Cross-verified all KPI calculations against baseline Python outputs (>95% accuracy target met)[cite: 5]. Verified zero missing/broken values and tested global filter reactivity[cite: 5].
2. **Filter Bookmarks Extension:** Deployed a standardized **Reset Filter Extension** across all 4 dashboard views to allow instant filter resets with a single click[cite: 4, 5].
3. **Documentation & Deliverables:** Prepared formal QA Checklists, Dashboard Testing Reports, and organized the project directory structure (`/data`, `/scripts`, `/dashboard`, `/docs`)[cite: 5].
4. **Portfolio Deployment:** Approved for deployment on GitHub and Tableau Public[cite: 5].

#### Milestone 4 Output
* QA Checklist Document (`QA_Checklist.pdf`)[cite: 5]
* Dashboard Testing Report (`Dashboard_Testing_Report.pdf`)[cite: 5]
* Final Tableau Workbook (`MedTrack_DV.twbx`)[cite: 5]
* Complete GitHub Repository structure[cite: 5]

---

### Project Status & Delivery Summary
The **MedTrack_DV** project has successfully completed all four milestones from data collection to final executive dashboard deployment[cite: 4, 5]. The resulting portfolio-ready dashboard suite provides hospital management with real-time operational visibility and data-driven decision-making tools[cite: 4, 5].

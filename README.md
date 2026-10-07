# Hospital Performance Intelligence System for Operational & Patient Care Analytics 🏥📊

![Project Name](https://img.shields.io/badge/Project-MedTrack__DV-blue?style=for-the-badge&logo=hospital)
![Theme](https://img.shields.io/badge/Theme-Executive%20Dark%20%230F172A-00F2FE?style=for-the-badge)
![Visualization](https://img.shields.io/badge/Visualization-Tableau%20Desktop%2FPublic-F59E0B?style=for-the-badge&logo=tableau)
![Data Wrangling](https://img.shields.io/badge/ETL-Python%20%7C%20Pandas-3776AB?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Completed%20%26%20Deployed-success?style=for-the-badge)

---

## 📌 Project Overview
**MedTrack_DV** is an executive-grade Hospital Performance Intelligence System designed to analyze hospital operations, patient flow dynamics, department performance, resource utilization, and clinical outcomes. The primary goal is to convert raw, disparate healthcare datasets into actionable operational intelligence for hospital administrators, department heads, and healthcare managers.

The dashboard suite utilizes an **Executive Dark Mode** (`#0F172A` background, `#1E293B` card containers) accented with glowing **Cyan (`#00F2FE`)** and **Amber (`#F59E0B`)** indicators for immediate visual clarity and high C-suite impact.

---

## 🌐 Live Interactive Dashboards & Previews

> 🔗 **[Click Here to Explore Live Tableau Dashboard](https://drive.google.com/file/d/1IdykGftatk46Od2CythAYZoLfaOh3eWr/view)

### 1️⃣ Hospital Overview
*High-level executive summary presenting hospital-wide operational status, total admissions, overall bed occupancy, and monthly inflow/outflow trends.*

[Hospital Overview Dashboard]<img width="1667" height="1027" alt="Screenshot 2026-10-07 132606" src="https://github.com/user-attachments/assets/de91d802-5a7a-4a96-a8dd-16946a0aeba2" />


### 2️⃣ Patient Flow Analytics
*Deep dive into patient intake dynamics, admission vs. discharge velocity, Average Length of Stay (ALOS) across departments, and readmission breakdown.*
[Patient Flow Dashboard]<img width="1650" height="831" alt="Screenshot 2026-10-07 132632" src="https://github.com/user-attachments/assets/fb563dca-6bba-4aca-9fe7-a30669c0503f" />


### 3️⃣ Department Analytics
*Comparative evaluation of departmental workload, capacity vs. occupancy treemaps, efficiency scoring, and clinical staff allocation.*
[Department Analysis Dashboard]<img width="1622" height="847" alt="Screenshot 2026-10-07 132650" src="https://github.com/user-attachments/assets/e7374bfb-b8ae-487f-a3d7-814fb5959ade" />



### 4️⃣ Resource Utilization
*Real-time asset tracking covering bed utilization rates, active clinical staff deployment (doctors/nurses), equipment status grids, and filter reset extension.*

[Resource Utilization Dashboard]<img width="1642" height="915" alt="Screenshot 2026-10-07 132705" src="https://github.com/user-attachments/assets/84b3db5e-bfe0-451f-a24d-dbd79d744b65" />



---
## MedTrack_DV – Complete Project Documentation (Milestone 1 to Milestone 4)



### Project Overview

**MedTrack_DV** is a Hospital Performance Intelligence System designed to analyze hospital operations, patient flow, department performance, resource utilization, and patient outcomes.

The project uses data preparation, validation, transformation, KPI development, and dashboarding to convert raw healthcare data into meaningful analytical insights for hospital management.



---



### Milestone 1 – Data Collection & Preparation

#### Objective

The objective of Milestone 1 was to collect the required hospital healthcare data, understand its structure, identify important analytical fields, and prepare the dataset for further cleaning and analysis.



#### Work Performed

**Data Collection:** The healthcare dataset was collected from Kaggle and loaded into the project environment using Python[cite: 4]. The raw dataset contains patient admission records along with hospital, department, admission, discharge, billing, test-result, and resource-related information[cite: 4].
2. **Data Understanding:** The dataset was examined to understand records, columns, data types, patient/hospital identifiers, admission/discharge info, department types, demographics, readmission info, and resource fields to build KPIs.

3. **Data Quality Assessment:** Initial data-quality checks were performed to identify missing values, duplicate records, incorrect data types, invalid date fields, and inconsistent categorical values.

4. **Data Cleaning & Preparation:** The raw data was processed using Python and data-cleaning notebooks to make the dataset consistent and analysis-ready[cite: 4].

5. **Clean Dataset Creation:** After cleaning, a standardized CSV dataset was generated as input for Milestone 2[cite: 4].

#### Milestone 1 Output

Raw healthcare dataset (`hospital_raw_data.csv`)
Cleaned healthcare dataset (`hospital_cleaned.csv`)
Data collection Python script (`data_collection.py`)
Data-cleaning Jupyter Notebook (`hospital_cleaning.ipynb`)


---

### Milestone 2 – KPI Development & Dashboard Preparation

#### Objective

The objective of Milestone 2 was to transform the cleaned hospital data into an analytical dataset, calculate the project's required KPIs, and prepare the initial dashboard structure for visualization.



#### Work Performed

**Cleaned Dataset Validation:** Verified fields like admissions, length of stay, readmission status, bed info, department, and waiting time before KPI calculations[cite: 4].
2. **KPI Development:** Python was used to calculate core hospital performance metrics:

   * **Total Admissions:** Measures total admission records.

   * **Occupancy Rate:** Proportion of occupied beds relative to total beds.

   * **Average Length of Stay (LOS):** Average number of days patients stay.

   * **Readmission Rate:** Percentage of patients identified as readmissions.

   * **Bed Utilization Rate:** Evaluates available bed capacity utilization.

   * **Department Efficiency:** Evaluates department-level operational performance.

3. **Analytical Dataset Preparation:** Exported final processed hospital data into Excel format for dashboard development.

4. **Dashboard Planning:** Prepared a dashboard storyboard defining structure, layout grids, and analytical flow[cite: 4].

5. **Tableau Prototype Development:** Created an initial Tableau prototype (`medtrack_prototype.twbx`) to verify visualization approach.



#### Milestone 2 Output

Final analytical dataset (`hospital_final_dataset.xlsx`)
KPI-generation Python script (`generate_hospital_kpis.py`)
Dashboard storyboard (`dashboard_storyboard.pdf`)
Tableau prototype (`medtrack_prototype.twbx`)


---



### Milestone 3 – Dashboard Development & Integration

#### Objective

The objective of Milestone 3 was to build and integrate the four core interactive Tableau dashboards using a modern executive dark theme (`#0F172A` background, `#1E293B` cards, Cyan `#00F2FE` and Amber `#F59E0B` accents).



#### Work Performed

**Hospital Overview Dashboard:** Built high-level executive KPIs, monthly occupancy trends, and top-level summaries.
2. **Patient Flow Dashboard:** Developed admission vs discharge tracking, average length of stay by department, and peak patient load analytics.

3. **Department Analytics Dashboard:** Created department efficiency comparisons, capacity vs occupancy tree maps, and medical staff distributions.

4. **Resource Utilization Dashboard:** Implemented bed utilization tracking, active clinical staff metrics, equipment utilization grids, and customized branding badge stickers.

5. **Dashboard Integration & Interactivity:** Configured global filters (Hospital, Department, Region, Date Range), parameter actions, and cross-tab navigation controls.



#### Milestone 3 Output

Integrated Tableau Workbook (`MedTrack_DV.twbx`)


---



### Milestone 4 – Testing, Validation & Delivery

#### Objective

The objective of Milestone 4 was to validate metrics, test dashboard interactivity, ensure zero calculation errors, and establish professional project documentation for portfolio deployment.



#### Work Performed

**Testing & Validation:** Cross-verified all KPI calculations against baseline Python outputs (>95% accuracy target met). Verified zero missing/broken values and tested global filter reactivity.
2. **Filter Bookmarks Extension:** Deployed a standardized **Reset Filter Extension** across all 4 dashboard views to allow instant filter resets with a single click.

3. **Documentation & Deliverables:** Prepared formal QA Checklists, Dashboard Testing Reports, and organized the project directory structure (`/data`, `/scripts`, `/dashboard`, `/docs`).

4. **Portfolio Deployment:** Approved for deployment on GitHub and Tableau Public.



#### Milestone 4 Output

QA Checklist Document (`QA_Checklist.pdf)
Dashboard Testing Report (`Dashboard_Testing_Report.pdf`)
Final Tableau Workbook (`MedTrack_DV.twbx`)
Complete GitHub Repository structure


## 📂 Repository Directory Structure

MedTrack_DV/
├── data/
│   ├── raw/                           # Kaggle raw hospital & admission datasets
│   │   └── hospital_raw_data.csv
│   └── processed/                     # Cleaned & transformed analytics datasets
│       ├── hospital_cleaned.csv
│       └── hospital_final_dataset.xlsx
├── scripts/
│   ├── data_collection.py             # Raw data fetch script
│   ├── hospital_cleaning.ipynb        # Data wrangling & cleaning notebook
│   └── generate_hospital_kpis.py      # Python KPI calculation engine
├── dashboard/
│   └── MedTrack_DV.twbx               # Complete 4-Page Tableau Workbook
├── docs/
│   ├── QA_Checklist.pdf               # Quality Assurance & Verification Matrix
│   ├── Dashboard_Testing_Report.pdf   # Dashboard Validation Report
│   └── dashboard_storyboard.pdf       # Storyboard layout wireframes
├── assets/                            # Dashboard Screenshots & Visuals
└── README.md                          # Project Documentation

### Project Status & Delivery Summary

The **MedTrack_DV** project has successfully completed all four milestones from data collection to final executive dashboard deployment. The resulting portfolio-ready dashboard suite provides hospital management with real-time operational visibility and data-driven decision-making tools.

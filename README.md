# 🏥 MedTrack_DV: Hospital Operations & Patient Care Analytics

[![Domain](https://img.shields.io/badge/Domain-Healthcare_Operations-blue.svg)](https://github.com)
[![Tools](https://img.shields.io/badge/Tools-Python_%7C_Tableau_%7C_Pandas-brightgreen.svg)](https://github.com)
[![Status](https://img.shields.io/badge/Status-Milestone_1_Completed-success.svg)](https://github.com)
[![Deliverable](https://img.shields.io/badge/Deliverable-MedTrack__DV.twbx-orange.svg)](https://github.com)

An end-to-end clinical intelligence and operational analytics suite designed to optimize patient flow, bed occupancy, department efficiency, and healthcare resource allocation using interactive Tableau dashboards.

---

## 📊 Executive Summary

| Attribute | Specification Details |
| :--- | :--- |
| **Project Name** | MedTrack_DV (Hospital Performance Intelligence System) |
| **Primary Goal** | Transform raw admission & operational records into actionable KPIs |
| **Core Architecture** | Data Pipeline (Python/Pandas) ➔ KPI Warehouse ➔ Tableau BI Suite |
| **Final Deliverable** | Unified 4-Tier Interactive Tableau Workbook (`MedTrack_DV.twbx`) |

---

## 🗺️ Project Milestones & Progress

| Milestone | Stage & Focus Area | Status | Deliverables Generated |
| :---: | :--- | :---: | :--- |
| **01** | **Data Collection & Cleaning** | `COMPLETED` | `hospital_raw_data.csv`<br>`data_collection.py`<br>`hospital_cleaning.ipynb`<br>`hospital_cleaned.csv` |
| **02** | **KPI Engineering & Storyboard** | `IN PROGRESS` | `hospital_final_dataset.xlsx`<br>`generate_hospital_kpis.py`<br>`dashboard_storyboard.pdf` |
| **03** | **Tableau Dashboard Suite** | `PENDING` | `MedTrack_DV.twbx`<br>(Overview, Flow, Dept, Utilization) |
| **04** | **Testing, QA & Documentation** | `PENDING` | `QA_Checklist.md`<br>`Dashboard_Testing_Report.md` |

---

## 📂 Repository Architecture

| Directory / File | Description & Purpose |
| :--- | :--- |
| 📁 `data/` | Raw ingested Kaggle datasets and preprocessed operational data files |
| 📁 `notebooks/` | Jupyter cleaning workflows, exploratory data analysis, and validation pipelines |
| 📁 `scripts/` | Standalone Python scripts for data ingestion and KPI computation algorithms |
| 📁 `dashboard/` | Tableau prototype (`.twbx`), storyboard wireframes, and final dashboards |
| 📁 `docs/` | Quality Assurance (QA) metrics validation sheets and testing protocols |
| 📄 `README.md` | Central project documentation and roadmap tracker |

---

## ⚙️ Tech Stack & Capabilities

| Layer | Tools & Frameworks | Applied Capabilities |
| :--- | :--- | :--- |
| **Data Ingestion** | Python, Kaggle API | Operational data collection, multi-source merging |
| **Data Engineering** | Pandas, NumPy | Schema normalization, missing value handling (<2%) |
| **Metric Formulation**| Python (KPI Engine) | ALOS, Occupancy Rate, Bed Utilization, Readmission Rate |
| **Business Intelligence**| Tableau Desktop / Public | Interactive charts, LOD expressions, dynamic actions |
| **Version Control** | Git, GitHub | Multi-branch collaborative workflow |

---

## 📈 Planned Dashboard Ecosystem

```text
               +-------------------------------------------+
               |           MedTrack_DV Workbook            |
               +---------------------+---------------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
         v                           v                           v
+------------------+       +-------------------+       +--------------------+
| Hospital Overview|       |   Patient Flow    |       | Dept & Utilization |
| - Total Admits   |       | - ALOS Metrics    |       | - Bed Occupancy    |
| - Regional Map   |       | - In vs Outflow   |       | - Dept Efficiency  |
+------------------+       +-------------------+       +--------------------+
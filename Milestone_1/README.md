# Milestone 1: Data Collection & Preparation

## Overview
Milestone 1 delivers the foundational data engineering and operational preparation for the **MedTrack Hospital Performance Intelligence System**. All operational healthcare source files have been collected, profiled, cleaned, and transformed into Tableau-ready star-schema analytical tables.

---

## Directory Structure

```text
Milestone_1/
├── data/
│   ├── raw/                                # Source operational files
│   │   ├── patients.csv                    (1,000 admissions, patient demographics)
│   │   ├── services_weekly.csv             (208 departmental weekly operational logs)
│   │   ├── staff_schedule.csv              (6,552 clinical shift assignments)
│   │   ├── staff.csv                       (110 clinical staff roster)
│   │   ├── hospital_insights_summary.csv   (208 weekly bed and operational records)
│   │   └── hospital-resource-utilization-dataset.csv
│   └── processed/                          # Cleaned, standardized, Tableau-ready datasets
│       ├── hospital_overview_dataset.csv   (1,000 rows × 14 cols) — Grain: 1 admission
│       ├── patient_flow_dataset.csv        (2,000 rows × 10 cols) — Grain: 1 movement event
│       ├── department_analytics_dataset.csv (208 rows × 12 cols)  — Grain: 1 dept + week
│       └── resource_utilization_dataset.csv (628 rows × 8 cols)   — Grain: 1 dept + week + role
├── docs/                                   # Data profiling & methodology reports
│   ├── dataset_sources.md                  (Dataset catalog & origins)
│   ├── methodology.md                      (Cleaning, normalization, and grain rules)
│   └── profiling_output.txt                (Full distribution & health profile)
├── notebooks/                              # Jupyter analysis & ETL pipelines
│   ├── 01_data_profiling.ipynb             (Initial profiling and exploratory analysis)
│   └── data_cleaning.ipynb                 (Production ETL and star-schema generator)
└── scripts/
    └── data_collection.py                  (Automated data collection and integrity verifier)
```

---

## Key Achievements & Quality Benchmarks

1. **Grain Isolation & Anti-Cartesian Design**:
   - Every analytical table has an explicitly defined grain (e.g., individual admission vs. weekly departmental aggregate) to prevent metric inflation during Tableau dashboard aggregations.

2. **Data Cleaning & Normalization**:
   - **Zero Duplicates**: Verified 0 duplicate records across all tables.
   - **Standardized Values**: Department names (`emergency`, `icu`, `surgery`, `general_medicine`) and staff roles unified.
   - **Prefix Formatting**: Identifiers standardized (`ADM-`, `PAT-`, `MOV-`, `RES-`).
   - **Temporal Modeling**: Extracted calendar dimensions (`year`, `month`, `quarter`, `day_of_week`) from raw timestamps.

3. **Data Quality Metrics**:
   - **Completeness**: Exceeds 99.8% across operational records (passing the >95% benchmark).
   - **Referential Integrity**: 100% foreign key matching across patient movements and admissions.

---

## How to Run & Verify

1. **Run Data Collection & Verification Script**:
   ```bash
   python Milestone_1/scripts/data_collection.py
   ```

2. **Execute Data Cleaning & ETL Pipeline**:
   - Open Jupyter:
     ```bash
     jupyter notebook Milestone_1/notebooks/data_cleaning.ipynb
     ```
   - Execute all cells to regenerate the processed datasets in `Milestone_1/data/processed/`.

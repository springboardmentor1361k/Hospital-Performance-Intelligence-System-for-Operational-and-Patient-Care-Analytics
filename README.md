# Hospital-Performance-Intelligence-System-for-Operational-and-Patient-Care-Analytics

## MedTrack_DV — Milestone 1: Data Collection & Preparation

This repository contains the completed **Milestone 1** work for the **MedTrack_DV Hospital Operations & Patient Care Analytics System**. The datasets have been collected, profiled, cleaned, validated, and structured into Tableau-ready datasets.

---

### Project Structure

```text
├── data/
│   ├── raw/                                # Original source operational files
│   │   ├── patients.csv
│   │   ├── services_weekly.csv
│   │   ├── staff_schedule.csv
│   │   ├── staff.csv
│   │   └── hospital_insights_summary.csv
│   └── processed/                          # Cleaned, standardized, Tableau-ready datasets
│       ├── hospital_overview_dataset.csv   (1,000 rows × 14 cols) — Grain: 1 admission
│       ├── patient_flow_dataset.csv        (2,000 rows × 10 cols) — Grain: 1 movement event
│       ├── department_analytics_dataset.csv (208 rows × 12 cols)  — Grain: 1 dept + week
│       └── resource_utilization_dataset.csv (628 rows × 8 cols)   — Grain: 1 dept + week + role
├── docs/                                   # Data dictionary & methodology documentation
│   ├── dataset_sources.md
│   ├── methodology.md
│   └── profiling_output.txt
├── notebooks/                              # Jupyter analysis & ETL notebooks
│   ├── 01_data_profiling.ipynb
│   └── data_cleaning.ipynb
├── .gitignore
├── requirements.txt
└── README.md
```

---

### Completed Milestone 1 Tasks

1. **Dataset Collection & Profiling**:
   - Organized core operational data covering admissions, departmental weekly flows, and clinical staff schedules.
   - Identified the unique grain of each operational dataset before merging or aggregation to prevent metric inflation.

2. **Data Cleaning & Normalization**:
   - **Deduplication**: Verified 0 duplicate rows across operational datasets.
   - **Text Standardization**: Normalized department names (`emergency`, `icu`, `surgery`, `general_medicine`) and role classifications.
   - **Identifier Formatting**: Standardized keys with stable prefixes (`ADM-`, `PAT-`, `MOV-`, `RES-`).
   - **Temporal Dimensions**: Cleaned and converted date fields (`arrival_date`, `departure_date`), deriving `year`, `month`, `quarter`, and `day_of_week`.

3. **Data Quality & Validation**:
   - **Missing Values**: 0% missing values in core admission records (exceeds the <2% missing value evaluation standard).
   - **Numeric Bounds**: Validated physiological ranges (Age ∈ [0, 120], LOS ≥ 0, Satisfaction ∈ [0, 100]).
   - **Relationship Integrity**: Ensured 100% referential integrity between patient movements and admissions.

4. **Tableau-Ready Output Generation**:
   - Saved 4 separated star-schema tables in `data/processed/` avoiding Cartesian product inflation.

---

### Setup & Reproducibility

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the cleaning notebook:
   - Launch Jupyter and run `notebooks/data_cleaning.ipynb` to regenerate all processed datasets in `data/processed/`.

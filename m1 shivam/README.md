MedTrack_DV/
│
├── data/
│   │
│   ├── raw/
│   │   └── Original hospital inpatient discharge datasets downloaded directly from the source.
│   │       No cleaning or modification should be performed here.
│   │
│   └── processed/
│       └── Cleaned, transformed, normalized, and analysis-ready datasets generated during the data pipeline.
│
│
├── notebooks/
│   │
│   ├── 01_data_loading.ipynb
│   │   └── Loads the raw dataset and performs initial exploration such as checking shape, columns, data types, and samples.
│   │
│   ├── 02_data_cleaning.ipynb
│   │   └── Handles missing values, duplicates, incorrect records, inconsistent formats, and unnecessary columns.
│   │
│   ├── 03_data_normalization.ipynb
│   │   └── Standardizes and transforms data into consistent formats, such as dates, categories, numerical values, and text.
│   │
│   ├── 04_data_validation.ipynb
│   │   └── Validates the processed dataset by checking data quality, constraints, ranges, missing values, and logical errors.
│   │
│   └── 05_kpi_engineering.ipynb
│       └── Creates healthcare and hospital KPIs required for analysis and visualization in the dashboard.
│
│
├── scripts/
│   │
│   ├── data_collection.py
│   │   └── Automatically downloads or collects the dataset from
│   │       Kaggle or another official data source and saves it inside \MedTrack_DV\data\raw.
│   │
│   └── generate_hospital_kpis.py
│       └── Automates the calculation and generation of hospital KPIs from the processed dataset.
│
│
├── dashboard/
│   │
│   └── MedTrack_DV.twbx
│       └── Tableau Packaged Workbook containing the interactive
│           MedTrack dashboard, visualizations, worksheets, dashboard design, and associated Tableau resources.
│
│
├── docs/
│   │
│   ├── dataset_sources.md
│   │   └── Documents where the dataset was obtained from, including source links, dataset descriptions,download instructions, and attribution.
│   │
│   ├── data_dictionary.md
│   │   └── Describes every important column in the dataset, including column name, meaning, data type,
│   │       possible values, and business interpretation.
│   │
│   ├── kpi_definitions.md
│   │   └── Defines every KPI used in the project, including its purpose, calculation formula, and interpretation.
│   │
│   ├── methodology.md
│   │   └── Explains the complete project workflow:
│   │
│   │       Data Collection
│   │              ↓
│   │       Data Loading
│   │              ↓
│   │       Data Cleaning
│   │              ↓
│   │       Data Normalization
│   │              ↓
│   │       Data Validation
│   │              ↓
│   │       KPI Engineering
│   │              ↓
│   │       Dashboard Development
│   │
│   └── testing_report.md
│       └── Contains data validation results, testing procedures,
│           identified issues, fixes applied, and final quality
│           verification of the project.
│
│
├── README.md
│   └── Main project documentation shown when someone opens
│       your GitHub repository.
│
│       It should include:
│       • Project Overview
│       • Problem Statement
│       • Project Objectives
│       • Dataset Information
│       • Technology Stack
│       • Project Architecture
│       • Installation Instructions
│       • How to Run the Project
│       • KPI Summary
│       • Dashboard Screenshots
│       • Key Insights
│       • Future Improvements
│
│
└── .gitignore
    └── Specifies files and folders that should not be uploaded
        to GitHub, such as large datasets, cache files,
        virtual environments, and secret/API key files.
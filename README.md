# Hospital Performance Intelligence System for Operational and Patient Care Analytics

**MedTrack_DV** is an end-to-end enterprise healthcare operational intelligence and clinical quality analytics system. The repository is organized into dedicated milestone directories to ensure modularity, clear governance, and reproducible analytics.

---

## Milestone Directory Navigation

| Milestone | Title | Focus Area | Directory Link |
| :--- | :--- | :--- | :--- |
| **Milestone 1** | **Data Collection & Preparation** | Raw dataset profiling, ETL normalization, star-schema data modeling, and data quality validation. | [Milestone_1/](file:///d:/Downloads/info/Milestone_1/README.md) |
| **Milestone 2** | **Dashboard Storyboard & KPI Specification** | Tableau visual architecture, 3 executive dashboards, 5 novel operational KPIs, and benchmark scorecards. | [Milestone_2/](file:///d:/Downloads/info/Milestone_2/README.md) |

---

## Repository Architecture

```text
├── Milestone_1/                                    # Milestone 1: Data Collection & Preparation
│   ├── data/
│   │   ├── raw/                                    # Source operational files (patients, services, staff)
│   │   └── processed/                              # Cleaned, standardized, Tableau-ready star-schema tables
│   ├── docs/                                       # Data dictionary, profiling outputs & methodology
│   ├── notebooks/                                  # Data profiling and production ETL notebooks
│   ├── scripts/                                    # Automated data loading and integrity verifier
│   └── README.md                                   # Milestone 1 documentation & reproducibility guide
│
├── Milestone_2/                                    # Milestone 2: Dashboard Storyboard & KPI Framework
│   ├── data/                                       # Department KPI summaries & hospital scorecards
│   ├── docs/                                       # KPI mathematical specifications & visual catalog
│   ├── reports/                                    # Executive visual presentation & storyboard PDF
│   └── README.md                                   # Milestone 2 dashboard architecture documentation
│
├── .gitignore                                      # Environment and cache ignore configuration
├── LICENSE                                         # Project open-source license
├── README.md                                       # Repository master index
└── requirements.txt                                # Python runtime dependencies
```

---

## Quick Start & Setup

1. **Environment Setup**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Milestone 1 Pipeline**:
   ```bash
   python Milestone_1/scripts/data_collection.py
   ```

4. **Explore Milestone 2 Storyboard & KPIs**:
   - Review [Milestone_2/docs/kpi_definitions_milestone2.md](file:///d:/Downloads/info/Milestone_2/docs/kpi_definitions_milestone2.md) for formulas and novel metrics.
   - Review [Milestone_2/docs/dashboard_storyboard_alternative_designs.md](file:///d:/Downloads/info/Milestone_2/docs/dashboard_storyboard_alternative_designs.md) for the visual encoding design catalog.
   - Open [Milestone_2/reports/Milestone 2.pdf](file:///d:/Downloads/info/Milestone_2/reports/Milestone%202.pdf) for the executive storyboard report.

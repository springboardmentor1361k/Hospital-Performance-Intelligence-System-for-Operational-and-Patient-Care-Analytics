# Hospital Performance Intelligence System for Operational and Patient Care Analytics

**MedTrack_DV** is an end-to-end enterprise healthcare operational intelligence and clinical quality analytics system. The repository is organized into dedicated milestone directories to ensure modularity, clear governance, and reproducible analytics.

---

## Milestone Directory Navigation

| Milestone | Title | Focus Area | Directory Link |
| :--- | :--- | :--- | :--- |
| **Milestone 1** | **Data Collection & Preparation** | Raw dataset profiling, ETL normalization, star-schema data modeling, and data quality validation. | [Milestone_1/](Milestone_1/README.md) |
| **Milestone 2** | **Dashboard Storyboard & KPI Specification** | Tableau visual architecture, 3 executive dashboards, 5 novel operational KPIs, and benchmark scorecards. | [Milestone_2/](Milestone_2/README.md) |
| **Milestone 3** | **Interactive Tableau Dashboards** | Hospital overview, patient clinical flow trajectories, department analysis, and resource utilization. | [Milestone_3/](Milestone_3/README.md) |
| **Milestone 4** | **Data Testing & Dashboard Verification** | Primary/foreign key integrity, Python/Pandas KPI re-computation, defect isolation, filter and navigation QA. | [Milestone_4/](Milestone_4/README.md) |

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
├── Milestone_3/                                    # Milestone 3: Tableau Analytical Dashboards
│   ├── reports/                                    # Exported Tableau executive reports & PDF dashboards
│   └── README.md                                   # Milestone 3 dashboard architecture documentation
│
├── Milestone_4/                                    # Milestone 4: QA, Data Testing & Verification
│   ├── docs/                                       # Audit logs and edge-case findings
│   ├── reports/                                    # Executive verification presentations & slide decks
│   ├── README.md                                   # Milestone 4 summary documentation
│   └── report.md                                   # Comprehensive Milestone 4 QA & Verification Report
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
   - Review [Milestone_2/docs/kpi_definitions_milestone2.md](Milestone_2/docs/kpi_definitions_milestone2.md) for formulas and novel metrics.
   - Review [Milestone_2/docs/dashboard_storyboard_alternative_designs.md](Milestone_2/docs/dashboard_storyboard_alternative_designs.md) for the visual encoding design catalog.
   - Open [Milestone_2/reports/Milestone 2.pdf](Milestone_2/reports/Milestone%202.pdf) for the executive storyboard report.

5. **Review Milestone 3 Tableau Visual Analytics**:
   - Open [Milestone_3/reports/Infosys_Milestone3_Dashboard_Export.pdf](Milestone_3/reports/Infosys_Milestone3_Dashboard_Export.pdf) to inspect the 3 interactive dashboards.

6. **Review Milestone 4 QA & Verification Deliverables**:
   - Open the presentation deck: [Milestone_4/reports/medtrackppt.pptx](Milestone_4/reports/medtrackppt.pptx).
   - Read the comprehensive verification, filter, and navigation report: [Milestone_4/report.md](Milestone_4/report.md).
   - Explore the live interactive workbook: [Tableau Public Live Dashboard](https://public.tableau.com/app/profile/vikram.simha.m.k/viz/Infosys_17914708025670/).

# Milestone 2: Tableau Dashboard Storyboard & KPI Architecture

## Overview
Milestone 2 specifies the business intelligence dashboard storyboard, visual encoding catalog, and multi-tier Key Performance Indicator (KPI) framework for the **MedTrack Hospital Performance Intelligence System**. 

The design establishes 3 interconnected executive dashboards replacing generic single-bar/donut charts with publication-grade analytical patterns (dual-axis horizon ribbons, 100-cell waffle matrices, clinical target bullet graphs, and 4-quadrant strategic matrices).

---

## Directory Structure

```text
Milestone_2/
├── data/                                   # Milestone 2 analytical datasets & scorecard exports
│   ├── department_kpi_summary_milestone2.csv (Department-level performance metrics & efficiency scores)
│   └── hospital_kpi_scorecard_milestone2.csv (Overall hospital KPI scorecard with targets & status)
├── docs/                                   # Storyboard design & KPI specifications
│   ├── kpi_definitions_milestone2.md       (Comprehensive mathematical formulas, benchmarks & rationales)
│   └── dashboard_storyboard_alternative_designs.md (Visual comparison: standard vs differentiated designs)
└── reports/
    └── Milestone 2.pdf                     # Visual submission presentation & dashboard mockups
```

---

## Dashboard Architecture

### Dashboard 1: Hospital Overview & Demand Intake Horizon
- **Strategic Purpose**: Real-time executive operational situational awareness, measuring inpatient admission throughput, bed saturation, and critically, unserved community healthcare demand.
- **Core Visuals**:
  - *Dual-Axis Area & Horizon Ribbon*: Plots `SUM(patients_request)` vs `SUM(patients_admitted)`, highlighting the 56.64% unmet turnaway gap.
  - *Hierarchical Treemap with Sparklines*: Department volume sized by tile area with viz-in-tooltip 12-week intake trajectory.
  - *100-Mark Waffle Matrix & Radial Gauge*: Active bed occupancy encoding (Emergency 100%, Surgery 88%).
  - *Clinical Target Bullet Graph*: Compares ALOS against the CMS/National clinical target benchmark (7.0 days).

### Dashboard 2: Patient Flow, Clinical Acuity & Care Quality
- **Strategic Purpose**: Inpatient clinical trajectories, diagnosis distributions, care experience, and readmission patterns.
- **Core Visuals**:
  - *Patient Acuity Sankey / Diverging Flow*: Intake Source → Department → Disease Diagnosis → Discharge Disposition.
  - *Box-and-Whisker Distribution Plot*: Shows median stay, IQR, and flags long-stay outliers (>14 days).
  - *Statistical Process Control (SPC) Funnel*: Readmission surveillance with 95% & 99.7% control limits.
  - *Disease Severity Bubble Matrix*: X = Volume, Y = ALOS, Size = Patient Satisfaction.

### Dashboard 3: Bed & Resource Intelligence (4-Quadrant Strategic Efficiency)
- **Strategic Purpose**: Physical bed capacity, clinical workforce saturation, and strategic resource allocation across hospital departments.
- **Core Visuals**:
  - *4-Quadrant Strategic Matrix*: Bed Utilization % (X) vs Demand Fulfillment % (Y), with bubble size = Workforce Stress Index.
  - *Capacity Utilization Bullet Chart*: Actual bed utilization against calibrated safety bands (<80% Safe, 80-85% Optimal, 85-95% High Risk, 100% Critical Overflow).
  - *Ward Strain Heatmap Calendar*: 2D matrix (Day of Week × Shift) colored from calm teal to urgent coral.
  - *Frontier Iso-Capacity Scatter Curve*: Surplus-bed units vs severely constrained units.

---

## Standard & Novel Key Performance Indicators (KPIs)

| KPI ID | KPI Name | Type | Value | Target / Benchmark |
| :--- | :--- | :--- | :---: | :---: |
| **KPI-01** | Total Admissions | Standard | 1,000 | 1,000 |
| **KPI-02** | Average Length of Stay (ALOS) | Standard | 7.41 days | < 7.00 days |
| **KPI-03** | Bed Occupancy Rate | Standard | 20.47% | 80.0% – 85.0% |
| **KPI-04** | Bed Utilization Rate | Standard | 92.47% | 85.0% |
| **KPI-05** | 30-Day Readmission Rate | Standard | 0.00% | < 5.0% |
| **KPI-06** | Department Efficiency Score | Standard | 88.45 / 100 | > 80.00 |
| **KPI-07** | **Patient Turnaway / Refusal Rate** | **Novel** | **56.64%** | < 20.0% |
| **KPI-08** | **Clinical Workforce Stress Index** | **Novel** | **88.98%** | < 80.0% |
| **KPI-09** | **Net Patient Satisfaction / Morale Index** | **Novel** | **80.00 / 100** | > 85.00 |

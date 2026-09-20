# MedTrack Milestone 2: Hospital Performance KPI Framework

This document outlines the Key Performance Indicator (KPI) architecture for the Hospital Performance Intelligence System, encompassing both core storyboard metrics and novel operational/clinical KPIs designed for our dataset.

---

## 1. Core Storyboard KPIs (Standard Foundation)

| KPI ID | KPI Name | Category | Formula | Value | Benchmark | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-01** | **Total Admissions** | Volume | $\sum \text{Unique Admission IDs}$ | **1,000** | Target: 1,000 | Baseline measure of inpatient demand and hospital throughput. |
| **KPI-02** | **Average Length of Stay (ALOS)** | Operational Throughput | $\frac{\sum \text{Length of Stay Days}}{\text{Total Admissions}}$ | **7.41 Days** | $< 7.0$ Days | Tracks patient progression efficiency; indicates post-acute bed blockages if elevated. |
| **KPI-03** | **Bed Occupancy Rate** | Capacity | $\frac{\text{Total Patient Days}}{\text{Available Beds} \times \text{Days}} \times 100\%$ | **20.47%** | $80\% - 85\%$ | Assesses aggregate licensed bed capacity vs active inpatient days across 52 weeks. |
| **KPI-04** | **Bed Utilization Rate** | Resource Efficiency | $\frac{\text{Active Beds in Use}}{\text{Total Operational Beds}} \times 100\%$ | **92.47%** | $85.0\%$ | Measures active operational bed stress (Emergency at 100%, General Medicine at 97.3%). |
| **KPI-05** | **30-Day Readmission Rate** | Clinical Quality | $\frac{\text{Unscheduled Readmissions}}{\text{Total Discharges}} \times 100\%$ | **0.00%** | $< 5.0\%$ | Standard clinical quality indicator for patient transition care and discharge readiness. |
| **KPI-06** | **Department Efficiency Score** | Composite Performance | Composite benchmark based on throughput, ALOS adherence, and capacity stability | **88.45 / 100** | $> 80.0$ | Evaluates multidisciplinary balance across hospital wings. |

---

## 2. Novel Differentiated KPIs (Unique to Our Dataset)

Standard hospital dashboards only track patients who are successfully admitted, completely missing unserved demand, capacity bottlenecks, and workforce burnout. Our data enables **3 differentiated performance metrics**:

### KPI-07: Patient Turnaway / Admission Refusal Rate (%)
* **Formula**:
  $$\text{Turnaway Rate} = \frac{\sum \text{Patients Refused}}{\sum \text{Patients Requested}} \times 100\% = \frac{7,642}{13,493} \times 100\% = \mathbf{56.64\%}$$
* **Inverse Metric (Demand Fulfillment Rate)**:
  $$\text{Demand Fulfillment Rate} = \frac{\sum \text{Patients Admitted}}{\sum \text{Patients Requested}} \times 100\% = \frac{5,851}{13,493} \times 100\% = \mathbf{43.36\%}$$
* **Why it's Differentiated**:
  - Other peer groups only observe the 1,000 admitted patients and assume hospital capacity is adequate.
  - Our metric proves that **over 56.6% of patient admission requests are turned away**, with **Emergency suffering an alarming 80.87% turnaway rate** due to critical bed and staff constraints.

---

### KPI-08: Clinical Workforce Stress & Utilization Index (%)
* **Formula**:
  $$\text{Workforce Utilization Index} = \text{Average}\left(\frac{\text{Clinical Staff In-Use}}{\text{Total Clinical Staff Available}}\right) \times 100\% = \mathbf{88.98\%}$$
* **Why it's Differentiated**:
  - Incorporates doctor, nurse, and nursing assistant shift logs from our resource utilization tracking.
  - Shows clinical saturation operating near critical thresholds ($88.98\%$), directly explaining the high turnaway rate.

---

### KPI-09: Caregiver Morale vs. Net Patient Satisfaction Index
* **Values**:
  - **Staff Morale Index**: **72.57 / 100** (Emergency lower at 68.4)
  - **Net Patient Satisfaction Index**: **80.00 / 100** (Benchmark $> 85.0$)
* **Why it's Differentiated**:
  - Connects staff burnout directly to patient satisfaction, giving hospital leadership an early-warning signal before clinical quality degrades.

---

## 3. Granular Department Performance Breakdown

| Department | Admissions | ALOS (Days) | Bed Util. (%) | Turnaway Rate (%) | Staff Util. (%) | Efficiency Score (/100) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Emergency** | 263 | 7.16 | **100.00%** | **80.87%** | 89.42% | 53.33 |
| **Surgery** | 254 | 7.87 | 88.19% | 24.77% | 89.82% | 74.36 |
| **General Medicine** | 242 | 7.00 | 97.32% | 45.39% | 87.66% | 67.85 |
| **ICU** | 241 | 7.61 | 84.38% | 17.87% | 89.03% | 77.64 |

---

## 4. Summary of Output Datasets

1. [`data/processed/hospital_kpi_scorecard_milestone2.csv`](file:///d:/Downloads/info/data/processed/hospital_kpi_scorecard_milestone2.csv)
2. [`data/processed/department_kpi_summary_milestone2.csv`](file:///d:/Downloads/info/data/processed/department_kpi_summary_milestone2.csv)

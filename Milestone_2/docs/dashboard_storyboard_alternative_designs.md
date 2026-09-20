# MedTrack Milestone 2: Advanced Dashboard Visual Design Architecture

This specification presents a **modern, differentiated visual analytics design** that replaces the basic, repetitive charts found in the Member 6 storyboard (`Milestone 2.pdf`).

---

## 1. Executive Summary of Design Paradigm Shifts

| Dimension | Member 6 Storyboard Design (`Milestone 2.pdf`) | Our Advanced Differentiated Design |
| :--- | :--- | :--- |
| **Visual Diversity** | 80% generic vertical/horizontal bar charts and donut charts. | Multi-tier visual hierarchy: Waffle Grid, Dual-Axis Area Ribbons, 4-Quadrant Strategic Matrix, Heatmaps, and Bullet Gauges. |
| **Data Redundancy** | Duplicate charts across tabs (e.g. *Admissions by Dept* and *Avg LOS* repeated in both D1 & D2). | Distinct, non-overlapping visual objectives for each dashboard view. |
| **Capacity Awareness** | Static occupied vs. available donut slice. | **Interactive 100-cell Bed Waffle Matrix** with real-time ward strain indicators. |
| **Demand Visibility** | Completely blind to unserved demand (only charts admitted count). | **Demand vs. Capacity Horizon Ribbon** displaying the 56.6% Turnaway / Care Gap. |
| **Efficiency Analysis** | 1D ranked bar chart of arbitrary efficiency score. | **4-Quadrant Efficiency Matrix** (Throughput vs. Bed Utilization with Workforce Stress bubble sizing). |

---

## 2. Detailed Chart-by-Chart Replacement Matrix

### Dashboard 1: Hospital Overview

| Original PDF Visual | Proposed Advanced Alternative | Visual Mechanics & Clinical Advantage |
| :--- | :--- | :--- |
| **Admissions Trend** *(Line chart)* | **Dual-Axis Demand vs. Capacity Area Ribbon** | Instead of a single line, plots **Patient Requests** (demand) against **Patients Admitted** (supply), shading the unmet gap (Turnaway zone) with a 7-day rolling moving average. |
| **Admissions by Department** *(Horizontal bar)* | **Hierarchical Treemap with Embedded Sparkbars** | Visualizes relative departmental volume as proportional area tiles with miniature sparklines showing 12-week admission velocity. |
| **Bed Status** *(Donut chart)* | **Interactive 100-Cell Bed Waffle Matrix & Radial Gauge** | Replaces low-density donut chart with an accessible grid where each tile represents hospital bed allocation colored by status (*Occupied, Reserved, Available, In-Turnaround*). |
| **Admissions by Type** *(Bar chart)* | **Diverging Stacked Intake Streamgraph** | Shows the temporal shift between Emergency (unplanned) vs Elective (scheduled) admissions across seasons and holiday surges. |
| **Average LOS by Department** *(Bar chart)* | **Box-Whisker / Target Bullet Graph** | Displays median stay, interquartile range (IQR), and long-stay outliers against the CMS/National clinical target benchmark (7.0 days). |

---

### Dashboard 2: Patient & Clinical Performance

| Original PDF Visual | Proposed Advanced Alternative | Visual Mechanics & Clinical Advantage |
| :--- | :--- | :--- |
| **Admissions by Department** *(Repeated bar)* | **Patient Acuity & Flow Sankey Diagram** | Maps patient intake channel $\rightarrow$ Department $\rightarrow$ Clinical Disease Category $\rightarrow$ Discharge disposition (*Home, Transfer, Deceased*). |
| **Average LOS by Department** *(Repeated bar)* | **Length of Stay Survival / Milestone Curve** | Cumulative discharge probability curve showing what percentage of patients are discharged within 3, 7, and 14 days per service. |
| **Readmission Rate by Department** *(Bar chart)* | **Statistical Process Control (SPC) Funnel Chart** | Plots departmental readmission rates against sample volume with 95% and 99.7% confidence control limits to distinguish common-cause vs special-cause variation. |
| **Admissions by Disease** *(Bar chart)* | **Disease Severity Bubble Matrix** | Bubbles plotted by Patient Volume (X), ALOS (Y), and Bubble Size (Total Resource Intensity / Cost). |
| **Admissions by Type** *(Donut chart)* | **Patient Age Demographics Population Pyramid** | Age bracket distribution by gender and admission urgency. |

---

### Dashboard 3: Bed & Department Performance

| Original PDF Visual | Proposed Advanced Alternative | Visual Mechanics & Clinical Advantage |
| :--- | :--- | :--- |
| **Bed Status** *(Stacked bar)* | **Bed Turnover Interval & Velocity Gauge** | Measures idle bed turnaround time (hours) between discharge and new patient bed-in. |
| **Beds by Ward** *(Bar chart)* | **Ward Strain Heatmap Calendar (Day × Shift)** | 2D matrix (Day of Week vs Shift) heat-mapped from cool green to urgent coral to pinpoint high-risk overflow times. |
| **Bed Utilization by Dept** *(Horizontal bar)* | **Capacity Utilization Bullet Graph with Warning Bands** | Bar displaying actual utilization against calibrated thresholds: Safe (<80%), Optimal (80-85%), High Risk (>85%), and Critical Overflow (100%). |
| **Department Efficiency Score** *(Ranked bar)* | **4-Quadrant Strategic Performance Matrix** | Scatter matrix mapping **Bed Utilization % (X)** vs **Demand Fulfillment % (Y)**, sized by **Staff Workforce Stress**: Top-right = High Performers, Top-left = Over-capacity Bottlenecks. |
| **Admissions vs Bed Capacity** *(Scatter plot)* | **Dynamic Frontier Iso-Capacity Scatter Curve** | Scatter plot with curved iso-utilization boundary lines highlighting under-resourced vs surplus-bed units. |

---

## 3. Design System & Accessibility Specifications

1. **Grid Architecture**: Rigid 8px spacing rhythm (`8px`, `16px`, `24px`, `32px`).
2. **Color Palette & Contrast**:
   - Primary Clinical Accent: `#0d9488` (Teal)
   - Capacity Warning: `#f59e0b` (Amber)
   - Overload / Turnaway Alert: `#ef4444` (Crimson)
   - Background Light: `#f8fafc` | Background Dark: `#0f172a`
   - Glassmorphic container panels with border highlights.
3. **Accessibility**: High contrast ratio ($\ge 4.5:1$), full keyboard focus states, semantic HTML5 elements, and `prefers-reduced-motion` compliance.

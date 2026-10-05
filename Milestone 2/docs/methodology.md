# Project Methodology

## 1. Dataset Preparation

The project uses four local CSV datasets identified in the README and Milestone 1 files: Hospital Overview, Patient Flow, Department Analytics, and Resource Utilization. The repository describes them as synthetic/local project data. No external healthcare API, hospital website, source URL, or data-generation procedure is recorded. The Milestone 1 data-collection script inventories and loads local raw files only.

## 2. Data Cleaning

The existing cleaning notebook removes exact duplicate rows, trims object/string fields, applies selected ID casing/whitespace standardization, maps selected patient-gender and admission-type values, and parses selected date fields. It writes the processed CSVs. It does not impute missing values. Department labels are not fully canonical by ID in the current processed files; this remains a documented quality item rather than an unrecorded correction.

## 3. Data Validation

The notebook checks exact duplicate rows, missing values, selected numeric bounds, and Patient Flow admission/patient references against Hospital Overview. The audit additionally verified declared record-grain keys, tested ID formats, parseable dates, and the two Patient Flow foreign-key relationships. Processed records had no exact duplicates or tested grain-key duplicates. Department-name variants and missingness remain; no acceptable completeness threshold is documented.

## 4. KPI Engineering

The KPI script and notebook calculate the six measures using the formulas documented in [KPI Definitions](kpi_definitions.md). The implementation uses separate datasets at their existing grains and does not merge the four dataframes. Department Efficiency Score is the mean of the existing `department_efficiency_score` field; its underlying composite components and weights are not present in the repository.

## 5. KPI Validation

The existing implementation asserts that Total Admissions is positive, Average Length of Stay is non-negative, and the four percentage/score measures are between 0 and 100. The values reproduced from processed data match the existing `KPI_Summary` worksheet. These checks establish reproducibility and basic ranges, not clinical validity or comparison to an external benchmark.

## 6. Tableau Data Preparation

The existing workbook contains a KPI summary and one worksheet per analytical dataset. The four source grains are admission, movement event, hospital-department-day, and hospital-department-date-resource-type. They must not be blindly physically joined: multiplying rows can duplicate counts, sums, and ratios. Use Tableau relationships or separate dashboard-level sources and preserve measure-specific aggregation.

## 7. Dashboard Planning

The README identifies four planned dashboards: Hospital Overview, Patient Flow, Department Analytics, and Resource Utilization. It also states that filters, navigation, comparisons, actions, and wireframes were planned. Detailed control behavior and visualization specifications are not recorded in inspectable text; see [Dashboard Plan](dashboard_plan.md) and verify the existing storyboard before treating those details as finalized.

## 8. Dashboard Design Principles

Project evidence supports a visual hierarchy/wireframe stage and a four-dashboard suite. Specific visual encodings, color rules, accessibility requirements, and interaction patterns are unavailable in repository documentation. The plan therefore does not claim those details were implemented.

## 9. Handling Different Grains

Keep measures with their source grain: admission-level values in Hospital Overview, event-level values in Patient Flow, daily department values in Department Analytics, and daily resource-type values in Resource Utilization. Apply filters and aggregate within the source before combining results. A relationship is not a license to sum duplicated measures after a many-to-many expansion.

## 10. Avoiding Duplicated Metrics

Do not join all four fact-like datasets into one physical table for convenience. For each KPI, use the source dataset and aggregation written in the existing implementation. In particular, preserve distinct admission counts, row-level readmission flags, ratio-of-sums formulas, and the department-row mean; do not recompute the efficiency score or substitute a different denominator.

# KPI Definitions

These formulas reproduce the existing logic in [the KPI script](../scripts/generate_hospital_kpis.py) and [the KPI notebook](../notebooks/kpi_calculation_analysis.ipynb). They are not substituted with alternative healthcare conventions. Dataset grains are documented in the [Milestone 1 data dictionary](../../Milestone%201/docs/data_dictionary.md).

## 1. Total Admissions

- **Business purpose:** Count distinct admission records in the hospital overview data.
- **Formula:** `nunique(admission_id)`.
- **Source:** Hospital Overview, one row per admission; field `admission_id`.
- **Tableau guidance:** Count distinct admission IDs at the selected filter scope; avoid counting duplicated admission rows after joins.
- **Interpretation:** Number of distinct admission IDs represented in the selected records.

## 2. Occupancy Rate

- **Business purpose:** Express occupied-bed counts relative to the recorded bed-count total.
- **Formula:** `sum(occupied_beds_count) / sum(total_beds) * 100`.
- **Source:** Department Analytics, one row per hospital + department + day; fields `occupied_beds_count`, `total_beds`.
- **Tableau guidance:** Apply the same ratio-of-sums calculation to Department Analytics. Do not sum precomputed percentages or physically multiply daily rows through joins.
- **Interpretation:** Percentage produced by the project's summed counts over the selected Department Analytics rows. The project does not document a different time-weighting rule.

## 3. Average Length of Stay

- **Business purpose:** Summarize recorded admission length of stay.
- **Formula:** `mean(length_of_stay_days)`.
- **Source:** Hospital Overview, one row per admission; field `length_of_stay_days`.
- **Tableau guidance:** Use the arithmetic mean of the admission-level field at the intended filter scope; preserve admission grain.
- **Interpretation:** Mean recorded length of stay in days across included admission rows.

## 4. Readmission Rate

- **Business purpose:** Report the share of admission rows marked as readmissions.
- **Formula:** `count(readmission_flag == "Yes") / number_of_hospital_overview_rows * 100`.
- **Source:** Hospital Overview, one row per admission; fields `readmission_flag` and admission-row count.
- **Tableau guidance:** Reproduce the row-level flag count divided by row count. Do not reinterpret it as a patient-level or time-window readmission rate; no such rule is implemented or documented.
- **Interpretation:** Percentage of included admission rows whose flag is exactly `Yes`.

## 5. Bed Utilization Rate

- **Business purpose:** Express bed units in use relative to available bed units.
- **Formula:** Filter Resource Utilization to `resource_type` whose trimmed, case-folded value is `bed`, then calculate `sum(units_in_use) / sum(total_units_available) * 100`.
- **Source:** Resource Utilization, one row per hospital + department + date + resource type; fields `resource_type`, `units_in_use`, `total_units_available`.
- **Tableau guidance:** Filter to Bed before calculating the ratio of sums. Keep the resource grain and avoid multiplying rows with other fact tables.
- **Interpretation:** Percentage of available bed units represented as in use across the selected bed-resource rows.

## 6. Department Efficiency Score

- **Business purpose:** Aggregate the department efficiency score already present in the department dataset.
- **Formula implemented:** `mean(department_efficiency_score)` across Department Analytics rows.
- **Source:** Department Analytics, one row per hospital + department + day; field `department_efficiency_score`.
- **Tableau guidance:** Reproduce the arithmetic mean over the same department-day rows. Do not derive a new score or substitute a weighted mean without an approved project definition.
- **Interpretation:** Mean of the stored score values across included department-day rows; observed source values are on a 0-100 scale.
- **Composite methodology and weights:** The repository does not contain the component formula or weights used to create `department_efficiency_score`. The KPI script does not calculate those components; it averages the existing field. Component weights are therefore unavailable and are not inferred here.

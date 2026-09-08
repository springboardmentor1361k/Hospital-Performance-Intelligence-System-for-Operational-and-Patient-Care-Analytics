# Methodology — MedTrack_DV Data Preparation (Milestone 1)

## 1. Grain defined for each processed table
- `hospital_overview_dataset.csv` — 1 row = 1 admission
- `patient_flow_dataset.csv` — 1 row = 1 movement event (Admission or Discharge)
- `department_analytics_dataset.csv` — 1 row = 1 department + week
- `resource_utilization_dataset.csv` — 1 row = 1 department + week + resource type

The 4 tables were kept separate rather than merged into one flat file, since their grains differ — a flat merge would inflate row counts and corrupt any KPI computed by simple counting.

## 2. patients.csv used as the single ground-truth patient source
`patients.csv` has 1,000 unique `patient_id`s, no nulls, no duplicates, and valid (non-negative) length-of-stay when `departure_date − arrival_date` is computed. It is the only file with real calendar dates instead of a numeric week index, so it was used as the authoritative source for Hospital Overview, and Department Analytics / Patient Flow were derived *from it* by aggregation, rather than pulled from a second, less consistent source.

## 3. Why services_weekly.csv and hospital_insights_summary.csv were NOT merged in as ground truth
Both files report a `patients_admitted` figure for the same week+service, but:
- They disagree with each other in 206 of 208 rows despite having the same column name.
- Neither reconciles with the true count from `patients.csv` (5,851 combined weekly admissions reported vs. 1,000 actual admissions in patients.csv).

Decision: these two files are treated as a separate, independently generated data source. They were **not** used to build the core Department Analytics numbers (those come from aggregating `patients.csv`). `services_weekly.available_beds` was kept as a **labeled reference field** (`available_beds_ref`) for an approximate bed-occupancy indicator, since it's the only bed-capacity figure available anywhere in the data — but it is documented as coming from a source that doesn't reconcile with the patient-level data, not as a verified capacity number.

## 4. Why staff_schedule.csv was used over staff.csv
- `staff.csv` reports 110 staff with per-service counts of 32/29/27/22.
- `staff_schedule.csv` reports 126 staff with per-service counts of 34/39/28/25 — which **exactly match** `hospital_insights_summary.staff_count` (34/39/28/25).
- The `staff_id` values in the two files don't overlap at all, and even matching by (name, role, service) only 33 of 110 staff.csv records line up.

Decision: `staff_schedule.csv` was treated as the authoritative staff roster and weekly-presence source (it's the one internally consistent with another file). `staff.csv` was excluded rather than force-reconciled.

## 5. Documented gaps (not fabricated)
Per the "don't force-fit / don't fabricate" rule, the following were left as documented gaps instead of being invented:
- **No equipment data** — none of the 5 core files contain equipment fields; the one file that does (`hospital-resource-utilization-dataset.csv`) belongs to a different, unrelated hospital system (see `dataset_sources.md`).
- **No true readmissions** — every `patient_id` in `patients.csv` is unique (no repeat visits), so `readmission_flag` is set to 0 for all rows and `readmission_rate_pct` is 0 in Department Analytics. This is a real limitation of the source data, not a computed zero.
- **No inter-department transfer data** — `patients.csv` records only one service per admission, so `patient_flow_dataset.csv` models each admission as a 2-step flow (Admission → Discharge) within a single department rather than true multi-department movement.
- **No time-of-day data** — `patients.csv` has dates only, not timestamps, so `hour_of_day`, `shift`, and `is_peak_hour` fields could not be derived and were left out of `patient_flow_dataset.csv` rather than filled with placeholder values.
- **Weekly, not daily, granularity** — `services_weekly.csv`, `staff_schedule.csv`, and `hospital_insights_summary.csv` are all indexed by week (1–52), not by date, so `department_analytics_dataset.csv` and `resource_utilization_dataset.csv` are built at weekly grain rather than the daily grain the original project brief described.

## 6. Cleaning steps applied
- Removed exact duplicate rows (0 found in any file).
- Standardized `service`/`role` text to lowercase/stripped values.
- Parsed all dates with `pd.to_datetime`; verified no nulls resulted.
- Verified no negative/impossible values: age in [0,120], length_of_stay ≥ 0.
- Derived `year`, `month`, `quarter`, `day_of_week` from `arrival_date`.
- No blanket `fillna(0)` was used anywhere — there were no missing values in any of the 5 raw files to begin with (confirmed in profiling, `docs/profiling_output.txt`).

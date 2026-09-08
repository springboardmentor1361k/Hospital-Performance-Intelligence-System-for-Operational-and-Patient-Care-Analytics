# Dataset Sources — MedTrack_DV

## Files used in the pipeline

| File | Rows × Cols | What it contains | Grain |
|---|---|---|---|
| `patients.csv` | 1,000 × 7 | Patient-level admissions: patient_id, name, age, arrival_date, departure_date, service, satisfaction | 1 row = 1 admission |
| `services_weekly.csv` | 208 × 10 | Weekly service-level snapshot: available_beds, patients_request/admitted/refused, satisfaction, staff_morale, event | 1 row = 1 service + week |
| `staff_schedule.csv` | 6,552 × 6 | Weekly staff presence per service/role (staff_id, week, present flag) | 1 row = 1 staff member + week |
| `hospital_insights_summary.csv` | 208 × 8 | Weekly service-level summary: patients_admitted, avg_stay, avg_satisfaction, max_occupancy, staff_count, recommended_staff | 1 row = 1 service + week |

All 4 files were provided directly (not downloaded fresh from a public catalog during this project), so no external URL is recorded for them — they're treated as the project's given raw data and kept unmodified in `data/raw/`.

## Files investigated but excluded

| File | Reason for exclusion |
|---|---|
| `staff.csv` (110 × 4) | Staff counts per service (32/29/27/22) do not match `hospital_insights_summary.staff_count` (34/39/28/25), while `staff_schedule.csv`'s roster counts match exactly. Only 33 of 110 staff.csv records could be matched to staff_schedule.csv even by name+role+service. Treated as a stale/inconsistent secondary file and not used further. |
| `hospital-resource-utilization-dataset.csv` (200 × 18) | Covers 30 different hospitals (not the single hospital system the other 5 files describe), a different date range (2023–2024 vs. this system's 2025 dates), and a different department taxonomy (has Pediatrics, no general_medicine). No shared key with the other files, so it cannot be joined in. It is the only file with equipment fields, which is why the pipeline has no equipment data (see `methodology.md`). |

## Cross-file consistency check performed

`services_weekly.csv` and `hospital_insights_summary.csv` share a `patients_admitted` field for the same week+service, but the values disagree in 206 of 208 rows, and neither reconciles with the true admission count from `patients.csv` (5,851 vs. 1,000 total). This means these two files are independently generated and not numerically consistent with `patients.csv` — see `methodology.md` for how this was handled.

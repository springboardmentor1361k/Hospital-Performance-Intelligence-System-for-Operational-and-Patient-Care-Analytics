# Tableau Data Model — MedTrack_DV

**Milestone 2, Step: Tableau Data Model (before dashboard development)**

## Why Relationships, not Joins

The 4 processed tables have **different grains**:

| Table | Grain |
|---|---|
| `hospital_overview_dataset` | one row = one admission |
| `patient_flow_dataset` | one row = one movement event (2 per admission) |
| `department_analytics_dataset` | one row = department + day |
| `resource_utilization_dataset` | one row = department + day + bed |
| `resource_utilization_staff_snapshot` | one row = department + role (static) |

A traditional Tableau **Join** flattens tables into one physical row set at query time — joining `hospital_overview` (45,000 rows) with `patient_flow` (90,000 rows) via a normal join would fan out admission-level measures (e.g. Total Admissions would inflate because each admission now appears twice). This is exactly the problem the mentor's document warns about in Section 21 ("1 × 5 × 3 = 15 rows" example).

**Tableau Relationships** (the "noodle" canvas, not the join-with-Venn-diagram screen) solve this: they keep each table at its native grain and perform a context-aware, LOD-safe join **per worksheet**, only pulling in the fields actually used in that sheet. This is the mentor-recommended approach ("model appropriately... test whether relationships are causing duplicated measures").

## Relationship Diagram

```
hospital_overview_dataset  ──(admission_id, 1:many)──►  patient_flow_dataset
        │
        │ (department_id, many:many at department grain)
        ▼
department_analytics_dataset ──(department_id + date, 1:many)──► resource_utilization_dataset
        │
        │ (department_id, many:many — snapshot, no date)
        ▼
resource_utilization_staff_snapshot
```

## Relationship Setup (build in this order in Tableau's Data Source canvas)

1. **`hospital_overview_dataset` ↔ `patient_flow_dataset`**
   - Key: `admission_id`
   - Cardinality: One (hospital_overview) to Many (patient_flow) — each admission has exactly 2 flow events.
   - Referential integrity: All (every admission has both an Admission and Discharge event; verified in notebook `03_build_final_tables.ipynb`, shape check `90,000 = 45,000 x 2`).

2. **`hospital_overview_dataset` ↔ `department_analytics_dataset`**
   - Key: `department_id`
   - Cardinality: Many to Many (many admissions per department, many daily rows per department).
   - **Do NOT also relate on date** — `hospital_overview` has `admission_date`/`discharge_date` (a range per admission), not a single daily key; forcing a date relationship here would silently drop rows that don't match exactly.

3. **`department_analytics_dataset` ↔ `resource_utilization_dataset`**
   - Keys: `department_id` AND `date`
   - Cardinality: One (department_analytics, one row per dept+day) to Many (resource_utilization can have multiple resource-type rows per dept+day, though currently only `bed` is populated).

4. **`department_analytics_dataset` ↔ `resource_utilization_staff_snapshot`**
   - Key: `department_id` only (no date — this table is a static snapshot)
   - Cardinality: Many to Many.
   - **Important:** because this table has no date, any worksheet mixing a date-filtered chart with the staff snapshot will show the same staff numbers repeated across every date — this must be labeled clearly on the dashboard (see `dashboard_storyboard.md`, Dashboard 4) so it is never misread as a daily trend.

## Which Sheets Are Safe Together

| Sheet combination | Safe? | Note |
|---|---|---|
| hospital_overview fields only | ✅ | Native grain, no relationship crossed |
| hospital_overview + patient_flow fields | ✅ | 1:many via admission_id, Tableau aggregates correctly per admission |
| department_analytics + resource_utilization (beds) | ✅ | Matched grain (dept+day) |
| department_analytics + staff_snapshot | ⚠️ Use with caution | Staff numbers will repeat per date row — only show staff as a separate, non-date chart (per storyboard) |
| hospital_overview + resource_utilization directly | ⚠️ Avoid | These are not directly related in the model (only via department_analytics as the bridge) — mixing their fields in one sheet may produce Tableau's "no relationship path" warning or unintended cross-joins |

## Validation Test (do this once the data source is built, before building dashboards)

1. Drag `admission_id` (Count Distinct) onto a blank sheet using ONLY `hospital_overview_dataset` fields → confirm **45,000**.
2. Add any `patient_flow_dataset` field (e.g. `movement_type`) to the same sheet → re-check `admission_id` (Count Distinct) → must **still show 45,000**, not 90,000. If it changes, the relationship cardinality is set wrong.
3. Repeat the same check for `department_analytics` + `resource_utilization`: Total Admissions from department_analytics should not change when resource_utilization fields are added to the same view.

If any of these counts change unexpectedly, STOP and fix the relationship before proceeding to dashboard development — this is exactly the "duplicated measures" failure mode the mentor's document warns about.

## Data Source File Setup

Connect all 5 CSVs from `data/processed/` in one Tableau data source (`MedTrack_DV.twbx` → Data Source tab), built as relationships per the diagram above — not as a single flattened extract.
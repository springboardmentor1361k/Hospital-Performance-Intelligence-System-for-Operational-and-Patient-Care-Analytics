import pandas as pd

files_to_load = [
    'patient.csv', 'admission.csv', 'department.csv', 'ward.csv', 'bed.csv',
    'doctor.csv', 'employee.csv', 'staff_assignment.csv', 'disease.csv',
    'patient_diagnostic.csv', 'diagnostic_test.csv', 'prescription.csv',
    'drug.csv', 'drug_manufacturer.csv', 'drug_inventory.csv', 'billing.csv',
    'billing_detail.csv', 'patient_insurance.csv', 'insurance_provider.csv'
]

dataframes = {}

for f in files_to_load:
    table_name = f.replace('.csv', '')
    dataframes[table_name] = pd.read_csv(f'/content/{f}')
    print(f"Loaded {f}")

summary_list = []

print("\n--- Table Sizes ---")
for name, df in dataframes.items():
    summary_list.append({
        'Table': name,
        'Rows': df.shape[0],
        'Cols': df.shape[1],
        'Avg Missing %': 0.0,
        'Duplicate Rows': 0,
        'Orphan FKs': 0
    })
    print(f"Table: {name}, Shape: {df.shape}")

overview_df = pd.DataFrame(summary_list)
print("\n--- Quick Overview ---")
display(overview_df[['Table', 'Rows', 'Cols']])


for name, df in dataframes.items():
    print(f"\n--- Table: {name} ---")
    print("Column types:")
    df.info()
    print("First 5 rows:")
    display(df.head())


missing_pct_list = []

for name, df in dataframes.items():
    print(f"\nChecking missing values for {name}:")

    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df)) * 100

    missing_info = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percentages
    })
    missing_info = missing_info[missing_info['Missing Count'] > 0]

    if not missing_info.empty:
        print(f"Missing in {name}:")
        display(missing_info)

        high_missing = missing_info[missing_info['Missing Percentage'] > 5]
        if not high_missing.empty:
            print(f"  WARNING: Columns in {name} with > 5% missing:")
            display(high_missing)
    else:
        print(f"  No missing values in {name}.")

    avg_table_missing = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100 if df.shape[1] > 0 else 0
    overview_df.loc[overview_df['Table'] == name, 'Avg Missing %'] = avg_table_missing

print("\n--- Updated Overview with Missing % ---")
display(overview_df[['Table', 'Rows', 'Cols', 'Avg Missing %']])


print("\n--- reference_id Missingness by charge_type ---")

if 'billing_detail' in dataframes and 'charge_type' in dataframes['billing_detail'].columns and 'reference_id' in dataframes['billing_detail'].columns:
    b_detail = dataframes['billing_detail']

    missing_by_charge_type = b_detail.groupby('charge_type')['reference_id'].apply(
        lambda x: x.isnull().mean() * 100
    )

    display(missing_by_charge_type)

    mixed_charge_types = missing_by_charge_type[(missing_by_charge_type > 0) & (missing_by_charge_type < 100)]

    if mixed_charge_types.empty:
        print("CONCLUSION: Looks like reference_id is conditional, not broken.")
    else:
        print("WARNING: Mixed missing values for some charge_types. This might be a real issue.")
        display(mixed_charge_types)
else:
    print("Skipping check (missing table or cols).")


print("\n--- Date Dtype Checks ---")

date_cols = [
    'date_of_birth', 'admission_date', 'discharge_date', 'test_date',
    'bill_date', 'policy_start_date', 'policy_end_date', 'last_restock_date',
    'prescription_date'
]

for name, df in dataframes.items():
    for col in date_cols:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                print(f"  WARN: '{col}' in '{name}' is '{df[col].dtype}', should be datetime. Convert later.")

print("\n--- ID Dtype Consistency ---")
id_types = {}

for name, df in dataframes.items():
    for col in df.columns:
        if col.endswith('_id'):
            current_dtype = str(df[col].dtype)
            if col in id_types:
                if id_types[col] != current_dtype:
                    print(f"  WARNING: '{col}' type mismatch! Was {id_types[col]}, now {current_dtype} in '{name}'.")
            else:
                id_types[col] = current_dtype

print("\n--- Full Dupe Row Check ---")
for name, df in dataframes.items():
    dupe_count = df.duplicated().sum()
    overview_df.loc[overview_df['Table'] == name, 'Duplicate Rows'] = dupe_count

    if dupe_count > 0:
        print(f"  WARNING: {name} has {dupe_count} duplicate rows.")
    else:
        print(f"  {name}: No full duplicate rows.")

print("\n--- PK Dupe Check ---")
pks = {
    'patient': 'patient_id',
    'admission': 'admission_id',
    'department': 'department_id',
    'ward': 'ward_id',
    'bed': 'bed_id',
    'doctor': 'doctor_id',
    'employee': 'employee_id',
    'staff_assignment': 'assignment_id',
    'disease': 'disease_id',
    'patient_diagnostic': 'patient_diagnostic_id',
    'diagnostic_test': 'test_id',
    'prescription': 'prescription_id',
    'drug': 'drug_id',
    'drug_manufacturer': 'manufacturer_id',
    'drug_inventory': 'inventory_id',
    'billing': 'bill_id',
    'billing_detail': 'billing_detail_id',
    'patient_insurance': 'patient_insurance_id',
    'insurance_provider': 'insurance_provider_id'
}

for t_name, pk_col in pks.items():
    if t_name in dataframes:
        df = dataframes[t_name]
        if pk_col in df.columns:
            dupe_pk_count = df[pk_col].duplicated().sum()
            if dupe_pk_count > 0:
                print(f"  WARNING: {t_name} has {dupe_pk_count} duplicate PKs in '{pk_col}'.")
            else:
                print(f"  {t_name}: No duplicate PKs in '{pk_col}'.")
        else:
            print(f"  WARN: PK col '{pk_col}' not in {t_name}.")
    else:
        print(f"  WARN: Table '{t_name}' not loaded.")

print("\n--- Overview with Dupe Counts ---")
display(overview_df[['Table', 'Rows', 'Cols', 'Avg Missing %', 'Duplicate Rows']])


print("\n--- Categorical Value Checks ---")

cat_cols = [
    'gender', 'blood_group', 'admission_status', 'admission_type', 'department_type',
    'ward_type', 'bed_status', 'employment_type', 'payment_mode', 'payment_status',
    'disease_category', 'drug_category', 'coverage_percentage',
    'test_type', 'test_status', 'drug_form', 'drug_dosage_form', 'manufacturer_name',
    'insurance_type'
]

for name, df in dataframes.items():
    for col in cat_cols:
        if col in df.columns and (pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col])):
            print(f"  Unique values for '{col}' in '{name}':")
            display(df[col].value_counts(dropna=False).head(10))

print("\n--- FK Integrity ---")

orphan_fks = {table: 0 for table in dataframes.keys()}

table_links = [
    ('admission', 'patient_id', 'patient', 'patient_id'),
    ('admission', 'bed_id', 'bed', 'bed_id'),
    ('admission', 'ward_id', 'ward', 'ward_id'),
    ('admission', 'department_id', 'department', 'department_id'),
    ('admission', 'disease_id', 'disease', 'disease_id'),
    ('bed', 'ward_id', 'ward', 'ward_id'),
    ('ward', 'department_id', 'department', 'department_id'),
    ('patient_diagnostic', 'admission_id', 'admission', 'admission_id'),
    ('patient_diagnostic', 'doctor_id', 'doctor', 'doctor_id'),
    ('patient_diagnostic', 'test_id', 'diagnostic_test', 'test_id'),
    ('prescription', 'admission_id', 'admission', 'admission_id'),
    ('prescription', 'drug_id', 'drug', 'drug_id'),
    ('drug', 'manufacturer_id', 'drug_manufacturer', 'manufacturer_id'),
    ('drug_inventory', 'drug_id', 'drug', 'drug_id'),
    ('billing', 'admission_id', 'admission', 'admission_id'),
    ('billing_detail', 'bill_id', 'billing', 'bill_id'),
    ('patient_insurance', 'patient_id', 'patient', 'patient_id'),
    ('patient_insurance', 'insurance_provider_id', 'insurance_provider', 'insurance_provider_id'),
    ('staff_assignment', 'employee_id', 'employee', 'employee_id'),
    ('staff_assignment', 'ward_id', 'ward', 'ward_id'),
    ('doctor', 'employee_id', 'employee', 'employee_id')
]

for ref_t_name, fk_col, pk_t_name, pk_col in table_links:
    if ref_t_name in dataframes and pk_t_name in dataframes:
        ref_df = dataframes[ref_t_name]
        pk_df = dataframes[pk_t_name]

        if fk_col in ref_df.columns and pk_col in pk_df.columns:
            fk_values = ref_df[fk_col].dropna().unique()
            pk_values = pk_df[pk_col].dropna().unique()
            orphan_values = pd.Series(fk_values)[~pd.Series(fk_values).isin(pk_values)].tolist()

            if orphan_values:
                print(f"  WARN: {len(orphan_values)} orphans in '{ref_t_name}.{fk_col}'. E.g., {orphan_values[:5]}")
                orphan_fks[ref_t_name] += len(orphan_values)
print("\n--- Admission/Bed/Ward Consistency ---")
if 'admission' in dataframes and 'bed' in dataframes and 'ward' in dataframes and 'department' in dataframes:
    adm_df = dataframes['admission'].copy()
    bed_df = dataframes['bed'].copy()
    ward_df = dataframes['ward'].copy()
    dept_df = dataframes['department'].copy()

    adm_bed_mrg = pd.merge(
        adm_df,
        bed_df[['bed_id', 'ward_id']].add_suffix('_from_bed'),
        left_on='bed_id', right_on='bed_id_from_bed', how='left'
    )

    adm_b_w_mrg = pd.merge(
        adm_bed_mrg,
        ward_df[['ward_id', 'department_id']].add_suffix('_from_ward'),
        left_on='ward_id_from_bed', right_on='ward_id_from_ward', how='left'
    )

    ward_mismatches = adm_b_w_mrg[
        (adm_b_w_mrg['ward_id'].notna()) &
        (adm_b_w_mrg['ward_id_from_bed'].notna()) &
        (adm_b_w_mrg['ward_id'] != adm_b_w_mrg['ward_id_from_bed'])
    ]

    if not ward_mismatches.empty:
        print(f"  WARN: {len(ward_mismatches)} admissions have ward_id mismatching bed.ward_id.")
        orphan_fks['admission'] += len(ward_mismatches)
    else:
        print("  Admission.ward_id matches bed.ward_id. Good.")

    dept_mismatches = adm_b_w_mrg[
        (adm_b_w_mrg['department_id'].notna()) &
        (adm_b_w_mrg['department_id_from_ward'].notna()) &
        (adm_b_w_mrg['department_id'] != adm_b_w_mrg['department_id_from_ward'])
    ]

    if not dept_mismatches.empty:
        print(f"  WARN: {len(dept_mismatches)} admissions have department_id mismatching ward.department_id.")
        orphan_fks['admission'] += len(dept_mismatches)
    else:
        print("  Admission.department_id matches ward.department_id. Good.")
else:
    print("  Skipping consistency check (missing tables).")

for table_name, count in orphan_fks.items():
    overview_df.loc[overview_df['Table'] == table_name, 'Orphan FKs'] = count

print("\n--- Overview with Orphan FKs ---")
display(overview_df[['Table', 'Rows', 'Cols', 'Avg Missing %', 'Duplicate Rows', 'Orphan FKs']])


print("\n--- Admission Status vs Bed Status ---")

if 'admission' in dataframes and 'bed' in dataframes:
    adm_df = dataframes['admission']
    bed_df = dataframes['bed']

    discharged_adms = (adm_df['admission_status'] == 'discharged').sum()
    total_adms = len(adm_df)

    occupied_beds = (bed_df['bed_status'] == 'occupied').sum()
    total_beds = len(bed_df)

    print(f"Discharged admissions: {discharged_adms} of {total_adms}")
    print(f"Occupied beds: {occupied_beds} of {total_beds}")

    if discharged_adms == total_adms and occupied_beds > 0:
        print("WARN: All patients discharged, but beds still occupied. This is an inconsistency.")
        print("  Will use `bed.bed_status` for Occupancy Rate KPI.")
    else:
        print("No major contradiction here. Ok.")
else:
    print("Skipping check (missing table).")


print("\n--- Date Logic ---")

if 'admission' in dataframes and 'admission_date' in dataframes['admission'].columns and 'discharge_date' in dataframes['admission'].columns:
    adm_df = dataframes['admission'].copy()
    adm_df['adm_dt'] = pd.to_datetime(adm_df['admission_date'], errors='coerce')
    adm_df['dis_dt'] = pd.to_datetime(adm_df['discharge_date'], errors='coerce')

    bad_discharge_dates = adm_df[
        (adm_df['adm_dt'].notna()) &
        (adm_df['dis_dt'].notna()) &
        (adm_df['dis_dt'] < adm_df['adm_dt'])
    ]

    if not bad_discharge_dates.empty:
        print(f"  WARN: {len(bad_discharge_dates)} admissions have discharge before admission.")
        display(bad_discharge_dates[['admission_id', 'adm_dt', 'dis_dt']].head())

print("\n--- Future Dates ---")
current_date = pd.Timestamp.now()

check_dates = [
    'date_of_birth', 'admission_date', 'discharge_date', 'test_date',
    'bill_date', 'policy_start_date', 'policy_end_date', 'last_restock_date',
    'prescription_date'
]

for name, df in dataframes.items():
    for col in check_dates:
        if col in df.columns:
            dt_series = pd.to_datetime(df[col], errors='coerce')
            future_dates = dt_series[(dt_series.notna()) & (dt_series > current_date)]
            if not future_dates.empty:
                print(f"  WARN: {len(future_dates)} future dates in '{name}.{col}'. E.g., {future_dates.iloc[0]}")


print("\n--- Unrealistic Numbers (e.g., negative) ---")
check_nums = [
    'total_beds', 'dosage', 'duration_days', 'standard_cost', 'unit_cost',
    'current_stock', 'quantity', 'age', 'sale_price', 'purchase_price',
    'insurance_amount', 'bill_amount', 'discount_amount', 'patient_share'
]

for name, df in dataframes.items():
    for col in check_nums:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            neg_values = df[col][df[col] < 0]
            if not neg_values.empty:
                print(f"  WARN: {len(neg_values)} negative values in '{name}.{col}'. E.g., {neg_values.iloc[0]}")


print("\n--- Final Project Summary ---")

display(overview_df[[
    'Table',
    'Rows',
    'Cols',
    'Avg Missing %',
    'Duplicate Rows',
    'Orphan FKs'
]])

comp_percent = (1 - (overview_df['Avg Missing %'] / 100)).mean() * 100
avg_missing_percent = overview_df['Avg Missing %'].mean()

print(f"\nOverall Completeness: {comp_percent:.2f}%")
print(f"Overall Avg Missing: {avg_missing_percent:.2f}%")

if comp_percent >= 95 and avg_missing_percent <= 2:
    print("\nCool, data looks good enough. Moving on.")
else:
    print("\nUH OH: Data might need more work. Review the warnings.")


nat_counts = {}

print("\n--- Converting Dates ---")
for name, df in dataframes.items():
    for col in date_cols:
        if col in df.columns:
            initial_nat = df[col].isnull().sum()
            dataframes[name][col] = pd.to_datetime(df[col], errors='coerce')
            new_nats = dataframes[name][col].isnull().sum() - initial_nat

            if new_nats > 0:
                print(f"  '{name}.{col}': Converted, {new_nats} new NaTs.")
            nat_counts[f'{name}.{col}'] = dataframes[name][col].isnull().sum()

print("\n--- ID Type Check (again) ---")
id_types_cleaned = {}
for name, df in dataframes.items():
    for col in df.columns:
        if col.endswith('_id'):
            current_dtype = str(df[col].dtype)
            if col in id_types_cleaned:
                if id_types_cleaned[col] != current_dtype:
                    print(f"  WARN: '{col}' type changed post-cleaning! This is bad: {current_dtype} in '{name}'.")
            else:
                id_types_cleaned[col] = current_dtype

print("  ID types still look consistent.")


print("\n--- Standardizing Text ---")

for name, df in dataframes.items():
    for col in cat_cols:
        if col in df.columns and pd.api.types.is_object_dtype(df[col]):
            dataframes[name][col] = df[col].str.strip().str.lower()

print("reference_id missingness (from Phase 1):")
display(missing_by_charge_type)


print("\n--- Making `length_of_stay` ---")

if 'admission' in dataframes and 'admission_date' in dataframes['admission'].columns and 'discharge_date' in dataframes['admission'].columns:
    adm_df = dataframes['admission']

    adm_df['length_of_stay'] = (adm_df['discharge_date'] - adm_df['admission_date']).dt.days

    print(f"  'length_of_stay' added to 'admission'.")

    if not adm_df[adm_df['length_of_stay'] < 0].empty:
        print(f"  WARN: Found negative 'length_of_stay' values.")
else:
    print("Skipping 'length_of_stay' (missing table/cols).")


print("\n--- Post-Cleaning Checks ---")

print("  Re-checking dupes:")
all_dupes_clean = True
for name, df in dataframes.items():
    if df.duplicated().sum() > 0:
        print(f"    WARN: '{name}' still has duplicates.")
        all_dupes_clean = False

print("\n  Re-checking NaT counts in date columns:")
all_nats_consistent = True
for name, df in dataframes.items():
    for col in date_cols:
        if col in df.columns:
            current_nat_count = df[col].isnull().sum()
            original_nat_count = nat_counts.get(f'{name}.{col}', 0)

            if current_nat_count != original_nat_count:
                print(f"    WARN: '{name}.{col}': NaT count changed ({original_nat_count} -> {current_nat_count}).")
                all_nats_consistent = False

print("\n--- Saving Cleaned DataFrames ---")

saved_files = []
for name, df in dataframes.items():
    output_filename = f'/content/{name}_cleaned.csv'
    df.to_csv(output_filename, index=False)
    saved_files.append(output_filename)
    print(f"  Saved '{name}' to '{output_filename}'.")

print("\n--- Done Saving ---\n")
print("Files saved:")
for f_path in saved_files:
    print(f"- {f_path}")

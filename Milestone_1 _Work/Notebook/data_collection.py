"""
============================================================
MedTrack_DV - Module 1: Hospital Data Collection
============================================================
Project     : MedTrack_DV (Hospital Operations & Patient
              Analytics Dashboard)
Milestone   : 1 - Data Collection and Preparation
Module      : 1 - Hospital Data Collection

Dataset Source : Kaggle
Dataset Name   : Healthcare Dataset
Author         : Prasad Patil
URL            : kaggle.com/datasets/prasad22/healthcare-dataset

Dataset Info:
    - Rows    : 55,500
    - Columns : 18
    - Format  : CSV

Data Collected:
    - Patient admission records
    - Hospital and department information
    - Admission and discharge dates
    - Billing and test results

Deliverable : hospital_raw_data.csv
============================================================
"""

import pandas as pd
import os

# ─────────────────────────────────────────────
# STEP 1: Dataset load
# ─────────────────────────────────────────────
print("=" * 55)
print("MedTrack_DV — Module 1: Data Collection")
print("=" * 55)

file_path = "hospital_raw_data.csv"

if not os.path.exists(file_path):
    print(f"\nError: '{file_path}' file not found")
    print("healthcare_dataset.csv name change with hospital_raw_data.csv karo.")
else:
    df = pd.read_csv(file_path)

    # ─────────────────────────────────────────────
    # STEP 2: Basic dataset info
    # ─────────────────────────────────────────────
    print(f"\nDataset Successfully Loaded!")
    print(f"\nShape      : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"File Size  : {os.path.getsize(file_path) / (1024*1024):.2f} MB")

    print(f"\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2}. {col}")

    # ─────────────────────────────────────────────
    # STEP 3: Sample data 
    # ─────────────────────────────────────────────
    print(f"\nSample Data (first 5 rows):")
    print(df.head().to_string())

    # ─────────────────────────────────────────────
    # STEP 4: Dataset completeness check
    # ─────────────────────────────────────────────
    print(f"\nDataset Completeness Check:")
    total_cells  = df.shape[0] * df.shape[1]
    null_cells   = df.isnull().sum().sum()
    completeness = ((total_cells - null_cells) / total_cells) * 100

    print(f"  Total Cells   : {total_cells:,}")
    print(f"  Null Cells    : {null_cells:,}")
    print(f"  Completeness  : {completeness:.2f}%")

    if completeness >= 95:
        print(f"  Status        : PASS (Target >95%) ✓")
    else:
        print(f"  Status        : FAIL (Target >95%) ✗")

    # ─────────────────────────────────────────────
    # STEP 5: Key columns verify
    # ─────────────────────────────────────────────
    print(f"\nKey Columns Verification:")

    key_cols = {
        "patient_id"        : "Patient identifier",
        "patient_age"       : "Patient age",
        "patient_gender"    : "Patient gender",
        "hospital_name"     : "Hospital name",
        "department"        : "Department name",
        "admission_type"    : "Admission type",
        "admission_date"    : "Admission date",
        "discharge_date"    : "Discharge date",
        "is_readmission"    : "Readmission flag",
        "total_beds"        : "Total beds",
        "occupied_beds"     : "Occupied beds",
        "doctors_count"     : "Doctors count",
        "nurses_count"      : "Nurses count",
        "equipment_total"   : "Equipment total",
        "equipment_in_use"  : "Equipment in use",
    }

    for col, desc in key_cols.items():
        status = "✓ Found" if col in df.columns else "✗ Missing"
        print(f"  {status} — {col} ({desc})")

    # ─────────────────────────────────────────────
    # STEP 6: Summary
    # ─────────────────────────────────────────────
    print(f"\n{'=' * 55}")
    print(f"Data Collection Summary")
    print(f"{'=' * 55}")
    print(f"  Source       : Kaggle — Prasad22 Healthcare Dataset")
    print(f"  Rows         : {len(df):,}")
    print(f"  Columns      : {len(df.columns)}")
    print(f"  Completeness : {completeness:.2f}%")
    print(f"  Duplicates   : {df.duplicated().sum()}")
    print(f"  Output File  : hospital_raw_data.csv")
    print(f"\n  Next Step    : Module 2 — Data Cleaning")
    print(f"  Run          : hospital_cleaning.ipynb")
    print(f"{'=' * 55}")

import os
import pandas as pd


def load_kaggle_raw_dataset():
    """
    Module 1: Load and verify raw hospital data from Kaggle.
    Ensures dataset completeness matches delivery evaluation criteria.
    """
    raw_data_path = os.path.join("data", "hospital_raw_data.csv")

    if not os.path.exists(raw_data_path):
        print(
            f"[ERROR] File not found at {raw_data_path}. Please place your Kaggle CSV inside the 'data/' folder and rename it to 'hospital_raw_data.csv'."
        )
        return

    df = pd.read_csv(raw_data_path)

    print("\n--- Dataset Summary ---")
    print(f"Total Records: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print("\nColumns detected:")
    print(list(df.columns))

    # Check Completeness Evaluation Metric (>95%)
    completeness = (1 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))) * 100
    print(f"\nDataset Completeness: {completeness:.2f}% (Target: >95%)")


if __name__ == "__main__":
    load_kaggle_raw_dataset()

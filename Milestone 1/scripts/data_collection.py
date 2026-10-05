"""Load MedTrack project CSVs from the local raw-data folder.

The repository describes these as synthetic/local project datasets. This script
uses only the provided files; it does not scrape websites or call healthcare
services. It inventories the inputs without editing or copying them.
"""

from pathlib import Path

import pandas as pd


MILESTONE_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = MILESTONE_ROOT / "data" / "raw"
DATASETS = {
    "Hospital Overview": "hospital_overview_dataset.csv",
    "Patient Flow": "patient_flow_dataset.csv",
    "Department Analytics": "department_analytics_dataset.csv",
    "Resource Utilization": "resource_utilization_dataset.csv",
}


def load_local_datasets():
    """Load the four approved raw CSV datasets without modifying source files."""
    datasets = {}
    for name, filename in DATASETS.items():
        path = RAW_DATA_PATH / filename
        if not path.is_file():
            raise FileNotFoundError(f"Required local dataset not found: {path}")
        datasets[name] = pd.read_csv(path)
    return datasets


def main():
    """Print a basic inventory of the local project inputs."""
    for name, frame in load_local_datasets().items():
        print(f"{name}: {len(frame)} rows, {len(frame.columns)} columns")


if __name__ == "__main__":
    main()

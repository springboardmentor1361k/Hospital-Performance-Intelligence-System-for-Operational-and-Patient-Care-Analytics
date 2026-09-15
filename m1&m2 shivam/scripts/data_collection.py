# Responsible for getting raw datasets from their original source
# and saving them inside data/raw/

import kagglehub
import shutil
from pathlib import Path


DATASETS = {
    "Hospital HMIS Dataset for Healthcare Analytics":
        "shalakagangurde/hospital-hmis-dataset-for-healthcare-analytics",

    "Hospital Beds Management":
        "jaderz/hospital-beds-management",

    "Hospital Data for Patient Readmission Prediction":"prasad22234/hospital-data-for-patient-readmission-prediction"
}


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def collect_data():
    """Download all datasets from Kaggle and store them in data/raw/."""

    for folder_name, dataset_id in DATASETS.items():

        # Create separate folder for each dataset
        dataset_raw_dir = RAW_DATA_DIR / folder_name
        dataset_raw_dir.mkdir(parents=True, exist_ok=True)

        print("=" * 60)
        print(f"Downloading: {folder_name}")
        print("=" * 60)

        # Download dataset from Kaggle
        downloaded_path = kagglehub.dataset_download(dataset_id)

        print(f"Dataset downloaded to cache: {downloaded_path}")

        # Copy downloaded files to project's raw data directory
        for item in Path(downloaded_path).iterdir():

            destination = dataset_raw_dir / item.name

            if item.is_file():
                shutil.copy2(item, destination)

            elif item.is_dir():
                shutil.copytree(
                    item,
                    destination,
                    dirs_exist_ok=True
                )

        print(f"Data successfully copied to:")
        print(dataset_raw_dir)
        print()


if __name__ == "__main__":
    collect_data()
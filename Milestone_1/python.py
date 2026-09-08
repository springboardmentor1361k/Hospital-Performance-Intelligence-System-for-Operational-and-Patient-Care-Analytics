import pandas as pd
from pathlib import Path


# --------------------------------------------------
# 1. DEFINE PROJECT DIRECTORIES
# --------------------------------------------------

DATA_DIR = Path("hospital_data")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. LOAD ALL CSV FILES
# --------------------------------------------------
DATA_DIR=Path("hospital_data")
data = {}

for file_path in DATA_DIR.glob("*.csv"):
    table_name = file_path.stem
    data[table_name] = pd.read_csv(file_path)

print("Hospital datasets loaded successfully.")

for table_name, df in data.items():
    print(f"{table_name}: {df.shape}")

print("\n--- Dataset Columns ---")
for table_name, df in data.items():
    print(f"{table_name}:{list(df.columns)}")


print("\n--- Running ID Standardization ---")

for table_name, df in data.items():
    # 1. Identify all ID columns dynamically
    id_cols = [col for col in df.columns if col.endswith('_id') or col.lower() in ['id', 'policy_number' ]]
    
    for col in id_cols:
        # 2. Convert to string, clean float decimals, and remove spaces
        df[col] = (df[col]
                   .astype(str)
                   .str.strip()
                   .str.replace(r'\.0$', '', regex=True))
        
        
     # 3. Unify missing or blank values into a clean blank entry
        df[col] = df[col].replace(['nan', 'none', 'null', '<na>', 'NAN'], '')

    print(f"✅ Standardized {len(id_cols)} ID fields in '{table_name}'")

print("\n🎉 ID Standardization complete!")

print("\n--- Running General Data & Department Standardization ---")

for table_name, df in data.items():
    # 1. Select all text columns, ignoring IDs and Dates
    text_cols = [
        col for col in df.select_dtypes(include=['object']).columns 
        if not col.endswith('_id') and col.lower() != 'id' and 'date' not in col.lower()
    ]
    
    for col in text_cols:
        # 2. Strip hidden spaces and handle missing values uniformly
        df[col] = df[col].fillna('').astype(str).str.strip()
        
        # 3. Apply targeted rules based on the column context
        if col.lower() == 'blood_group':
            df[col] = df[col].str.upper()   # Keeps blood types clean (e.g., 'A+', 'O-')
            
        elif col.lower() == 'icu' or col.lower() == 'room_no':
            df[col] = df[col].str.upper()   # Keeps acronyms standardized
            
        else:
            df[col] = df[col].str.title()   # Converts 'ward_name', 'city', 'gender', 'shift' to Title Case
            
        # 4. Fill empty entries with a standard placeholder
        df[col] = df[col].replace(['', 'Nan', 'None', 'Null', '<Na>'], 'Unknown')

    print(f"📝 Cleaned all text columns in dataset: '{table_name}'")

print("\n🎉 All text, department, and categorical data are completely standardized!")

print("\n--- Running Missing Value & Duplicate Handling ---")

for table_name, df in data.items():
    print(f"\n📊 Processing Dataset: '{table_name}'")
    
    # 1. DUPLICATE HANDLING
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    duplicate_count = initial_rows - len(df)
    if duplicate_count > 0:
        print(f"   🗑️ Removed {duplicate_count} exact duplicate rows.")
    else:
        print("   ✅ No exact duplicate rows found.")
        
    # 2. MISSING VALUE HANDLING (IMPUTATION)
    # Identify numeric and text/object columns separately
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    text_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Track missing values fixed
    missing_summary = {}
    
    # A. Handle missing values in Numeric columns using Median Imputation
    for col in numeric_cols:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            missing_summary[col] = f"Filled {missing_count} rows with Median ({median_val})"
            
    # B. Handle missing values in Text columns using a Placeholder
    for col in text_cols:
        # Check for both actual NaNs and residual invalid string indicators from imports
        invalid_markers = ['nan', 'none', 'null', '<na>', 'unknown', '']
        # Map values to lowercase for rigorous string validation
        is_missing = df[col].isna() | df[col].astype(str).str.lower().str.strip().isin(invalid_markers)
        missing_count = is_missing.sum()
        
        if missing_count > 0:
            df.loc[is_missing, col] = 'Unknown'
            missing_summary[col] = f"Filled {missing_count} rows with 'Unknown'"
            
    # Print summary of modifications for transparency
    if missing_summary:
        for col, msg in missing_summary.items():
            print(f"   🔧 Column '{col}': {msg}")
    else:
        print("   ✅ No missing values detected in numeric or categorical profiles.")
        
    # Update the global data dictionary reference with the cleaned dataframe
    data[table_name] = df

print("\n🎉 Missing value imputation and duplicate removal complete across all datasets!")

print("\n--- Exporting Clean CSV Files ---")

# 1. Automatically create a clean folder on your computer
OUTPUT_DIR = Path("cleaned_hospital_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Save all 9 datasets into the new folder
for table_name, df in data.items():
    output_path = OUTPUT_DIR / f"{table_name}_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"💾 Permanently Saved: {output_path}")

print("\n🎉 ALL DONE! Your fully cleaned datasets are saved on your disk.")
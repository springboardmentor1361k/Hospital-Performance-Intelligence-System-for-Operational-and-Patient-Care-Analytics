import pandas as pd

# 1. Load Cleaned Dataset
df = pd.read_csv('hospital_cleaned.csv')

# 2. Calculate 6 Core KPIs
total_admissions = len(df)
occupancy_rate = (df['occupied_beds'].sum() / df['total_beds'].sum()) * 100
avg_los = df['length_of_stay_days'].mean()
readmission_rate = (df['is_readmission'].sum() / total_admissions) * 100
bed_utilization = occupancy_rate
dept_efficiency = df.groupby('department')['avg_wait_time_hours'].mean().round(2).to_dict()

# 3. Print Results
print("--- MEDTRACK_DV KPI SUMMARY ---")
print(f"1. Total Admissions: {total_admissions}")
print(f"2. Occupancy Rate: {occupancy_rate:.2f}%")
print(f"3. Avg Length of Stay (LOS): {avg_los:.2f} Days")
print(f"4. Readmission Rate: {readmission_rate:.2f}%")
print(f"5. Bed Utilization Rate: {bed_utilization:.2f}%")
print(f"6. Department Efficiency: {dept_efficiency}")

# 4. Save Final Excel File (Using openpyxl engine)
df.to_excel('hospital_final_dataset.xlsx', index=False, engine='openpyxl')
print("File saved successfully as hospital_final_dataset.xlsx!")
import glob, os
import pandas as pd

DATA = "hospital_synthetic_shalaka/hospital_data"
T = {os.path.basename(f)[:-4]: pd.read_csv(f) for f in glob.glob(f"{DATA}/*.csv")}

PK = {
    "admission": "admission_id", "bed": "bed_id", "billing": "bill_id",
    "billing_detail": "billing_detail_id", "department": "department_id",
    "diagnostic_test": "test_id", "disease": "disease_id", "doctor": "doctor_id",
    "drug": "drug_id", "drug_inventory": "inventory_id",
    "drug_manufacturer": "manufacturer_id", "employee": "employee_id",
    "insurance_provider": "insurance_provider_id", "patient": "patient_id",
    "patient_diagnostic": "patient_diagnostic_id",
    "patient_insurance": "patient_insurance_id", "prescription": "prescription_id",
    "staff_assignment": "assignment_id", "ward": "ward_id",
}
FK = [  # (child, column, parent)
    ("admission", "patient_id", "patient"), ("admission", "department_id", "department"),
    ("admission", "ward_id", "ward"), ("admission", "bed_id", "bed"),
    ("admission", "disease_id", "disease"), ("bed", "ward_id", "ward"),
    ("billing", "admission_id", "admission"), ("billing_detail", "bill_id", "billing"),
    ("diagnostic_test", "department_id", "department"), ("doctor", "employee_id", "employee"),
    ("drug", "manufacturer_id", "drug_manufacturer"), ("drug_inventory", "drug_id", "drug"),
    ("employee", "department_id", "department"),
    ("patient_diagnostic", "admission_id", "admission"),
    ("patient_diagnostic", "test_id", "diagnostic_test"),
    ("patient_diagnostic", "doctor_id", "doctor"),
    ("patient_insurance", "patient_id", "patient"),
    ("patient_insurance", "insurance_provider_id", "insurance_provider"),
    ("prescription", "admission_id", "admission"), ("prescription", "drug_id", "drug"),
    ("staff_assignment", "employee_id", "employee"), ("staff_assignment", "ward_id", "ward"),
    ("ward", "department_id", "department"),
]
ONE_TO_ONE = {("billing", "admission_id"), ("doctor", "employee_id"),
              ("drug_inventory", "drug_id"), ("staff_assignment", "employee_id")}

print("== PRIMARY KEYS ==")
for t, c in PK.items():
    d = T[t]
    print(f"{t}.{c}: rows={len(d)} nulls={d[c].isnull().sum()} dups={d[c].duplicated().sum()}")

print("\n== FOREIGN KEYS ==")
for child, col, parent in FK:
    s = T[child][col]
    orphans = (~s.dropna().isin(T[parent][PK[parent]])).sum()
    o2o = "" if (child, col) not in ONE_TO_ONE else f" 1-to-1 ok={not s.duplicated().any()}"
    print(f"{child}.{col} -> {parent}: nulls={s.isnull().sum()} orphans={orphans}{o2o}")

print("\n== RELATIONSHIP / BUSINESS LOGIC ==")
a = T["admission"].copy()
a["admission_date"] = pd.to_datetime(a.admission_date)
a["discharge_date"] = pd.to_datetime(a.discharge_date)

# Finding 1: bill total vs line items
s = T["billing_detail"].groupby("bill_id").amount.sum().rename("line_sum")
b = T["billing"].set_index("bill_id").join(s)
diff = b.total_amount - b.line_sum
print("F1 mismatched bills:", (diff.abs() > 0.01).sum(),
      "| lower:", (diff < -0.01).sum(), "| higher:", (diff > 0.01).sum())

# Finding 2: bill date vs stay
m = T["billing"].merge(a, on="admission_id")
m["bill_date"] = pd.to_datetime(m.bill_date)
print("F2 bill before admission:", (m.bill_date < m.admission_date).sum(),
      "| outside stay:", ((m.bill_date < m.admission_date) | (m.bill_date > m.discharge_date)).sum())

# Finding 3: bed status vs admissions
bed = T["bed"]
print("F3 bed status:", bed.bed_status.value_counts().to_dict(),
      "| distinct beds used:", a.bed_id.nunique(),
      "| Occupied beds with any admission:",
      bed[bed.bed_status == "Occupied"].bed_id.isin(a.bed_id).sum())

# Finding 4: overlapping bed stays (two methods)
x = a.sort_values(["bed_id", "admission_date"]).copy()
same = x.bed_id == x.bed_id.shift()
prev_end = x.discharge_date.shift()
print("F4 overlap vs previous stay only:", (same & (x.admission_date < prev_end)).sum())
run_end = x.groupby("bed_id").discharge_date.cummax().groupby(x.bed_id).shift()
print("F4 overlap vs any earlier stay:", (x.admission_date < run_end).sum())

# Finding 5: department mismatches
pdg = T["patient_diagnostic"].merge(a[["admission_id", "department_id"]], on="admission_id")
pdg = pdg.merge(T["diagnostic_test"][["test_id", "department_id"]].rename(columns={"department_id": "test_dept"}), on="test_id")
doc = T["doctor"].merge(T["employee"][["employee_id", "department_id"]], on="employee_id")[["doctor_id", "department_id"]].rename(columns={"department_id": "doc_dept"})
pdg = pdg.merge(doc, on="doctor_id")
print("F5 test dept != admission dept:", (pdg.test_dept != pdg.department_id).sum(),
      "| doctor dept != admission dept:", (pdg.doc_dept != pdg.department_id).sum())
sa = T["staff_assignment"].merge(T["employee"], on="employee_id").merge(
    T["ward"][["ward_id", "department_id"]].rename(columns={"department_id": "ward_dept"}), on="ward_id")
print("F5 staff assigned outside own dept:", (sa.department_id != sa.ward_dept).sum(), "of", len(sa))

# Finding 6: insurance
pi = T["patient_insurance"].copy()
pi["s"] = pd.to_datetime(pi.policy_start_date); pi["e"] = pd.to_datetime(pi.policy_end_date)
h = a[a.patient_id.isin(pi.patient_id)].merge(pi, on="patient_id")
h["ok"] = (h.admission_date >= h.s) & (h.admission_date <= h.e)
g = h.groupby("admission_id").ok.any()
print("F6 insured admissions:", len(g), "| inside active policy:", g.sum())
bb = T["billing"].merge(a[["admission_id", "patient_id"]], on="admission_id")
no = bb[~bb.patient_id.isin(pi.patient_id)]
print("F6 bills, patient has no policy:", len(no), "| insurance_covered > 0:", (no.insurance_covered_amount > 0).sum())

# Finding 7: duplicate policy numbers / repeated pairs
print("F7 policy numbers used twice:", pi.policy_number.duplicated().sum(),
      "| repeated patient+provider rows:", pi.duplicated(["patient_id", "insurance_provider_id"]).sum())

# Finding 8: DOB after admission
z = a.merge(T["patient"], on="patient_id")
print("F8 admission before DOB:", (z.admission_date < pd.to_datetime(z.date_of_birth)).sum())

# Finding 9: reference_id nulls
bd = T["billing_detail"]
print("F9 null reference_id by type:", bd.reference_id.isna().groupby(bd.charge_type).sum().to_dict())

# Finding 11: info
print("F11 patients with no admission:", (~T["patient"].patient_id.isin(a.patient_id)).sum(),
      "| patients with >1 policy:", (pi.groupby("patient_id").size() > 1).sum())

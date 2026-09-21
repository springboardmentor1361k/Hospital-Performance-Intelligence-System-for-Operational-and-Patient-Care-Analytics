Clinical departments used for occupancy/bed KPIs: ['Emergency', 'ICU', 'Internal Medicine', 'Orthopedics', 'Pediatrics', 'Surgery']

======================================================================
KPI 1: TOTAL ADMISSIONS
======================================================================
Overall: 45000
department_name
Emergency             8777
ICU                   4040
Internal Medicine     7695
Orthopedics           5924
Pediatrics            8438
Surgery              10126
Name: total_admissions, dtype: int64

[cross-check] overall: hospital_overview=45000 vs department_analytics=45000 -> MATCH
[cross-check] by department: 0 department(s) mismatched

======================================================================
KPI 2: OCCUPANCY RATE  [estimated -- see note above]
======================================================================
Overall: 25.36%
department_name
Emergency            24.92
ICU                  28.15
Internal Medicine    25.01
Orthopedics          25.15
Pediatrics           25.66
Surgery              23.86
Name: occupancy_rate_pct, dtype: float64

[reasonableness check] max single-day occupancy observed across all departments: 58.0% (within plausible bounds)

======================================================================
KPI 3: AVERAGE LENGTH OF STAY
======================================================================
Overall: mean=5.16 days, median=4.0 days
                   mean  median
department_name                
Emergency          4.69     4.0
ICU                9.98    10.0
Internal Medicine  4.66     4.0
Orthopedics        4.68     4.0
Pediatrics         4.69     4.0
Surgery            4.67     4.0

[cross-check] direct (hospital_overview) vs re-weighted (department_analytics):
                   direct  reweighted_from_da  diff
department_name                                    
Emergency            4.69                4.69   0.0
ICU                  9.98                9.98   0.0
Internal Medicine    4.66                4.66   0.0
Orthopedics          4.68                4.68   0.0
Pediatrics           4.69                4.69   0.0
Surgery              4.67                4.67   0.0
-> MATCH

======================================================================
KPI 4: READMISSION RATE  [30-day proxy, not clinically verified]
======================================================================
Observed window ends 2026-01-12; eligibility cutoff = 2025-12-13
476 discharge(s) censored out of the denominator (too recent to have had a fair 30-day follow-up window)

Overall (eligibility-adjusted, documented default): 2.52%
Overall (naive, numerator/all admissions -- for reference only): 2.49%
department_name
Emergency            2.43
ICU                  2.76
Internal Medicine    2.58
Orthopedics          2.17
Pediatrics           2.51
Surgery              2.65
Name: readmission_rate_pct, dtype: float64

[cross-check] readmission count: hospital_overview=1120 vs department_analytics=1120 -> MATCH

======================================================================
KPI 5: BED UTILIZATION RATE
======================================================================
Overall: 25.36%
department_name
Emergency            24.92
ICU                  28.15
Internal Medicine    25.01
Orthopedics          25.15
Pediatrics           25.66
Surgery              23.86
Name: bed_utilization_pct, dtype: float64

[cross-check] Bed Utilization Rate vs Occupancy Rate (KPI 2), overall: 25.36% vs 25.36% -> MATCH

======================================================================
KPI 6: DEPARTMENT EFFICIENCY SCORE
======================================================================
                   occupancy_pct  avg_los  readmission_pct  department_efficiency_score
Pediatrics                 25.66     4.69             2.51                        60.13
Orthopedics                25.15     4.68             2.17                        60.05
Internal Medicine          25.01     4.66             2.58                        59.92
Emergency                  24.92     4.69             2.43                        59.85
Surgery                    23.86     4.67             2.65                        59.40
ICU                        28.15     9.98             2.76                        50.47
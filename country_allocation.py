"""
AIM:

To automatically assign delegates committees and countries

CONSTRAINTS:

Equal number of students of a particular grade in each committee
Preferably do not have people from same class in each committee

SOLUTION:

Have quotas for each grade in each committee, fill them for each grade
Sort by division and fill committies one delegate at a time alternatively (solves constraint 2)
"""

import random
import pandas as pd

committees = ["DISEC", "SC", "WHO", "UNODC", "ECOSOC", "UNHRC"]

countries = [
    "United States", "France", "Germany", "China", "India", "Brazil", "Mexico", "Canada",
    "Italy", "Spain", "Netherlands", "Sweden", "Finland", "Belgium", "Austria", "Norway",
    "Switzerland", "Denmark", "Japan", "South Korea", "Australia", "New Zealand", "Turkey",
    "Jordan", "Qatar", "United Arab Emirates", "South Africa", "Nigeria", "Kenya",
    "Democratic Republic of Congo", "Uganda", "Angola", "Zambia", "Morocco", "Tunisia", "Argentina"
]

country_matrix = {}
for i, committee in enumerate(committees):
    li = countries.copy()
    random.shuffle(li)
    country_matrix[committee] = li

delegates_df = pd.read_excel("Delegates.xlsx")

delegates = {row['First Name']: (row['Grade'], row['Section'])
    for _, row in delegates_df.iterrows() if row['Confirmed']==True}

def allocate_countries(delegates):
    grade_sort = {grade: [] for grade in ['VIII', 'IX', 'X', 'XI', 'XII']}
    output = []
    for delegate, class_ in delegates.items():
        print(class_[0])
        grade_sort[class_[0].strip()].append([delegate, *class_])

    for grade in grade_sort:
        grade_sort[grade.strip()].sort(key=lambda x: x[2])

    c = 0
    for grade in grade_sort:
        while grade_sort[grade]:
            delegate = grade_sort[grade].pop()
            committee = committees[c % len(committees)]
            country = country_matrix[committee].pop()
            output.append([*delegate, committee, country])
            c += 1

    return output

assigned = allocate_countries(delegates)
assigned_df = pd.DataFrame(assigned, columns=["First Name", "Grade", "Section", "Committee", "Country"])
updated_df = delegates_df.merge(assigned_df[["First Name", "Committee", "Country"]], on="First Name", how="left")
updated_df.to_excel("Delegates_Assigned.xlsx", index=False)

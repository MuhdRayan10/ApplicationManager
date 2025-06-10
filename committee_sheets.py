"""
AIM: To sort the (already assigned) delegates into their respective committees for their chairs to manage
"""

import pandas as pd

delegates_df = pd.read_excel("data/Delegates_Assigned.xlsx")
delegates = []
for _, row in delegates_df.iterrows():
    if row['Confirmed'] == True:
        delegates.append((row['First Name'], row['Email'], row['Grade']+'-'+row['Section'], row['Committee'], row['Country']))

# Now we sort by committee
committee_list = ["DISEC", "SC", "WHO", "UNODC", "ECOSOC", "UNHRC"]
committees = {committee:[] for committee in committee_list}

for delegate in delegates:
    committees[delegate[3]].append(delegate)


for committee, dels in committees.items(): 
    committee_df = pd.DataFrame(columns=["First Name", "Email", "Class", "Committee", "Country"])
    data = pd.DataFrame(dels, columns=["First Name", "Email", "Class", "Committee", "Country"])

    updated_df = pd.concat([committee_df, data], ignore_index=True)
    updated_df.to_excel(f"data/{committee}.xlsx", index=False)

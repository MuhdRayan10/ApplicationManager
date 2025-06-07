
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

committees = ["DISEC", "SC", "WHO", "UNODC", "ECOSOC", "UNHRC"]
country_matrix = {} #committee: countries left

def allocate_countries(delegates):
    grade_sort = {grade:[] for grade in ['IX', 'X', 'XI', 'XII']}
    output = []

    for delegate, class_ in delegates.items():
        grade_sort[class_[0]].append([delegate, *class_])

    for grade in grade_sort:
        grade_sort[grade].sort(key=lambda x:x[2]) 

        c = 0
        while grade_sort[grade]:
            delegate = grade_sort[grade].pop()
            committee = committees[c%6]
            country = country_matrix[committee].pop()


            output.append([*delegate, committee, country])

    return output








        

import sys
import pdb
import pandas as pd
import scipy.stats as st

fname = sys.argv[1]

df = pd.read_csv(fname)
print(df.head())
df = df[["Input.instruction", "Input.text_1", "Input.text_2", "Answer.comparisonReason", "Answer.creative_1.Creative Verse 1", "Answer.creative_2.Creative Verse 2", "Answer.fluency_1", "Answer.fluency_2", "Answer.instruction_1_1.yes", "Answer.instruction_1_2.no", "Answer.instruction_2_1.yes", "Answer.instruction_2_2.no"]]
print(df.head())
df = df.to_dict(orient='records')

items = {}
for row in df:
    # print(row)
    if row['Input.instruction'] not in items.keys():
        items[row['Input.instruction']] = []
    items[row['Input.instruction']].append(row)

tot_inst1 = []
tot_inst2 = []
tot_fl1 = []
tot_fl2 = []
tot_c1 = []
votes_c1 = []
votes_inst1 = []
votes_inst2 = []
votes_fl1 = []
votes_fl2 = [] 

agreement_c = []
agreement_f = []
agreement_i1 = []
agreement_i2 = []

for key in items.keys():
    item = items[key]
    c1 = 0
    fl1 = 0
    fl2 = 0
    inst1 = 0
    inst2 = 0
    for row in item:
        # print(row)
        if row["Answer.creative_1.Creative Verse 1"] == True:
            c1+=1
        fl1 += row["Answer.fluency_1"]
        fl2 += row["Answer.fluency_2"]
        inst1 += int(row["Answer.instruction_1_1.yes"] == True)
        inst2 += int(row["Answer.instruction_2_1.yes"] == True)
    # print(c1, fl1, fl2, inst1, inst2)
    if c1 >= 2:
        tot_c1.append(1)
    else:
        tot_c1.append(0)

    if c1 == 0 or c1 == 3:
        agreement_c.append(1)
    else:
        agreement_c.append(0)

    if inst1 >= 2:
        tot_inst1.append(1)
    else:
        tot_inst1.append(0)

    if inst1 == 3 or inst1 == 0:
        agreement_i1.append(1)
    else:
        agreement_i1.append(0)

    if inst2 >= 2:
        tot_inst2.append(1)
    else:
        tot_inst2.append(0)

    if inst2 == 3 or inst2 == 0:
        agreement_i2.append(1)
    else:
        agreement_i2.append(0)

    tot_fl1.append(fl1/3.0)
    tot_fl2.append(fl2/3.0)
    votes_c1.append(c1)
    votes_inst1.append(inst1)
    votes_inst2.append(inst2)
    votes_fl1.append(fl2)
    votes_fl2.append(fl1)

print("CV1 is better? ", sum(tot_c1)/len(tot_c1))# , tot_c1)
print("Agreement on which is better: ", sum(agreement_c)/len(agreement_c))
print("CV1 satisfies Instruction? ", sum(tot_inst1)/len(tot_inst1), votes_inst1) # , tot_inst1)
print("Agreement on Instruction CV1: ", sum(agreement_i1)/len(agreement_i1))
print("CV2 satisfies Instruction? ", sum(tot_inst2)/len(tot_inst2), votes_inst2)
print("Agreement on Instruction CV2: ", sum(agreement_i2)/len(agreement_i2))
print("Is CV1 fluent? ", sum(tot_fl1)/len(tot_fl1))#, votes_fl1)
print("Is CV2 fluent? ", sum(tot_fl2)/len(tot_fl2))#, votes_fl2)

r, p = st.pointbiserialr(tot_inst1, tot_fl1)
print("CV1: Correlation between fluency and success", r, p)
r, p = st.pointbiserialr(tot_inst2, tot_fl2)
print("CV2: Correlation between fluency and success", r, p)
temp = pd.crosstab(tot_inst1, tot_c1)
# print(temp)
r, p, dof, expected = st.chi2_contingency(temp)
print("CV1: Correlation between 1/0 creativity and success", r, p)
tot_c2 = [(i+1)%2 for i in tot_c1]
temp = pd.crosstab(tot_inst2, tot_c2)
# print(temp)
r, p, dof, expected = st.chi2_contingency(temp)
print("CV2: Correlation between 1/0 creativity and success", r, p)

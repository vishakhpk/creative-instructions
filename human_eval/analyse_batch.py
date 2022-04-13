import sys
import pdb
import pandas as pd

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

    if inst1 >= 2:
        tot_inst1.append(1)
    else:
        tot_inst1.append(0)

    if inst2 >= 2:
        tot_inst2.append(1)
    else:
        tot_inst2.append(0)

    tot_fl1.append(fl1/3.0)
    tot_fl2.append(fl2/3.0)

print("CV1 is better? ", sum(tot_c1)/len(tot_c1), tot_c1)
print("CV1 satisfies Instruction? ", sum(tot_inst1)/len(tot_inst1), tot_inst1)
print("CV2 satisfies Instruction? ", sum(tot_inst2)/len(tot_inst2), tot_inst2)
print("Is CV1 fluent? ", sum(tot_fl1)/len(tot_fl1), tot_fl1)
print("Is CV2 fluent? ", sum(tot_fl2)/len(tot_fl2), tot_fl2)

# pdb.set_trace()

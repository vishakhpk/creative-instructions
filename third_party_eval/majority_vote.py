import sys
import pandas as pd

f = sys.argv[1]

df = pd.read_csv(f)
print(df.keys())

batch = {}

for index, item in df.iterrows():
    if item['HITId'] not in batch.keys():
        batch[item['HITId']] = []
    batch[item['HITId']].append(item)

for k in batch.keys():
    assert len(batch[k]) == 3, print(k)

c_acc = 0
c_votes = []
s_acc = 0
s_votes = []

c_pref = 0
pref_votes = []
for k in batch.keys():
    c_temp = 0
    s_temp = 0
    c_pref_temp = 0
    for item in batch[k]:
        if item['Answer.accurate1-1.yes'] == True:
            c_temp+=1
        if item['Answer.accurate2-1.yes'] == True:
            s_temp+=1
        if item['Answer.creative1.creative1'] == True:
            c_pref_temp+=1
    c_votes.append(c_temp)
    s_votes.append(s_temp)
    pref_votes.append(c_pref_temp)
    # print(batch[k])
    # print(c_votes, s_votes, pref_votes)
    if c_temp > 1:
        c_acc+=1
    if s_temp > 1:
        s_acc+=1
    if c_pref_temp > 1:
        c_pref+=1

print("Is Collaborative Poem Accurate: ", c_acc/len(batch.keys()), c_acc, sum(c_votes), sum(c_votes)/(3*len(batch.keys())))
print("Is Solo Poem Accurate: ", s_acc/len(batch.keys()), s_acc, sum(s_votes), sum(s_votes)/(3*len(batch.keys())))
print("Is Collaborative Poem Preferred: ", c_pref/len(batch.keys()), c_pref, sum(pref_votes), sum(pref_votes)/(3*len(batch.keys())))

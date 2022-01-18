import json
import pdb
import re
import random
random.seed(0)

train_filename = "train.json"
val_filename = "val.json"

subj = []
with open(train_filename, 'r') as f:
    for line in f:
        obj = json.loads(line.strip())
        src = obj['translation']['en1']
        t = re.findall("'([^']*)'", src)
        t = list(set(t))
        if len(t) == 0:
            continue
        subj.extend(t)

print(len(subj))

seen_ent = []
unseen_ent = []
common = 0
c = 0
with open(val_filename, 'r') as f:
    for line in f:
        c += 1
        if c%1000 == 0:
            print(c)
        obj = json.loads(line.strip())
        src = obj['translation']['en1']
        t = re.findall("'([^']*)'", src)
        t = list(set(t))
        if len(t) == 0:
            seen_ent.append(obj)
            unseen_ent.append(obj)
            common+=1
            continue
        flag = True
        for item in t:
            # print(item, item in subj, flag)
            if item in subj:
                flag = False
                # print(item, item in subj, flag)
                break
        if flag:
            unseen_ent.append(obj)
        else:
            seen_ent.append(obj)

print(common, len(seen_ent), len(unseen_ent))

# ki_ke = random.sample(seen_ent, 50)
# ki_ue = random.sample(unseen_ent, 50)

with open("ki_ke.json", "w") as f:
    for item in seen_ent:
        f.write(json.dumps(item)+'\n')

with open("ki_ue.json", "w") as f:
    for item in unseen_ent:
        f.write(json.dumps(item)+'\n')


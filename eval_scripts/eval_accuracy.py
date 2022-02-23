import sys
import pdb
import json

fname = sys.argv[1] 

ip = []
with open(fname, 'r') as f:
    for line in f:
        ip.append(json.loads(line.strip()))

tot = 0
corr = 0
for item in ip:
    op = item['generation']
    pred = ""
    for token in op:
        if token is "":
            continue
        pred+=token+" "
    pred = pred.strip()
    ref = item['translation']['en2']
    if ref != pred:
        print("REFERENCE: ", ref)
        print("PREDICTION: ", pred)
        print("-"*40)
    # pdb.set_trace()
    if ref == pred:
        corr+=1
    tot+=1

print(float(corr)/tot, corr, tot)

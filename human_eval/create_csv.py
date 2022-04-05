import sys
import json

t5f = sys.argv[1]
gpt3f = sys.argv[2]
opf = sys.argv[3]

t5 = {}
gpt3 = {}

with open(t5f, 'r') as f:
    for line in f:
        obj = json.loads(line.strip())
        t5[obj['instruction']] = obj

with open(gpt3f, 'r') as f:
    for line in f:
        obj = json.loads(line.strip())
        gpt3[obj['instruction']] = obj

print(len(t5.keys()))
print(len(gpt3.keys()))

op = []
for key in gpt3.keys():
    assert key in t5.keys(), print(key)
    line = '"'+key+'","'+t5[key]['generation']+'","'+gpt3[key]['generation']+'"'
    op.append(line.replace("\n", ""))

with open(opf, 'w') as f:
    f.write("instruction,text_1,text_2\n")
    for item in op:
        f.write(item+'\n')


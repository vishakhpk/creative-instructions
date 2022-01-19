import sys
import json
import random
random.seed(0)

fname = sys.argv[1]

split_types = ['rhyme', 'simile', 'metaphor', 'haiku']
split_counts = [10, 5, 5, 5]
sample_size = 50

data = []
with open(fname, 'r') as f:
    for line in f:
        data.append(json.loads(line.strip()))

splits = {'misc': []}
for split in split_types:
    splits[split] = []

for item in data:
    assigned = False
    for split in split_types:
        if split in item['translation']['en1']:
            assigned = True
            splits[split].append(item)
            break
    if not assigned:
        splits['misc'].append(item)

for k in splits.keys():
    print(k, len(splits[k]))

test_set = []
for i, split in enumerate(split_types):
    test_set.append(random.sample(splits[split], split_counts[i]))

misc_count = sample_size - sum(split_counts)
test_set.append(random.sample(splits['misc'], misc_count))

test_data = [item for sublist in test_set for item in sublist]
print(len(test_data))

with open("sample-"+str(sample_size)+"-"+fname, 'w') as f:
    for item in test_data:
        f.write(json.dumps(item)+'\n')


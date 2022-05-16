import sys
import pronouncing
import json
import re
import syllapy
import scipy.stats as st
from datasets import load_metric

filename = sys.argv[1]

items = []
with open(filename, 'r') as f:
    for line in f:
        items.append(json.loads(line.strip()))


tot = 0
succ = 0
split = {}
tot_split = {}
for k in ['rhyme', 'simile', 'metaphor', 'haiku', 'end', 'start', 'subject']:
    split[k] = 0
    tot_split[k] = 0

for obj in items:
    src = obj['instruction'] #translation']['en1']
    tot+=1
    if 'rhymes with' in src:
        tot_split['rhyme']+=1
        t = re.findall("rhymes with '([^']*)'", src)
        t = list(set(t))
        if len(t) == 0:
            continue
        src_word = t[0]
        gen = obj['generation'] #translation']['en2']
        last_word = gen.split()[-1]
        flag = False
        for word in pronouncing.rhymes(src_word):
            if last_word in word or word in last_word:
                succ +=1
                split['rhyme']+=1
                break
    elif 'haiku' in src:
        tot_split['haiku']+=1
        t = re.findall("'([^']*)'", src)
        if len(t) == 0:
            continue
        gen = obj['generation']#'translation']['en2']
    
        subj = True
        for item in t:
            if item.lower() not in gen.lower():
                subj = False

        count = 0
        for word in gen.split():
            if word == '/':
                continue
            count+=syllapy.count(word)
        # print(gen, count)
        if subj and count >= 15 and count <= 19:
            succ+=1
            split['haiku']+=1
    elif "simile" in src:
        t = re.findall("'([^']*)'", src)
        tot_split['simile']+=1
        if len(t) == 0:
            continue
        gen = obj['generation']#'translation']['en2']
            # print(t, src, gen)
        comp = False
        subj = True
        for item in t:
            if item.lower() not in gen.lower():
                subj = False

        comp_list = ["is a", "is like a", "is an", "is like an", "is the", "is like the", 'like a', 'like the', "is like"]
        for item in comp_list:
            if item in gen:
                comp = True
        if subj and comp:
            succ += 1
            split['simile']+=1
    elif "metaphor" in src:
        t = re.findall("'([^']*)'", src)
        tot_split['metaphor']+=1
        if len(t) == 0:
            continue
        gen = obj['generation']#'translation']['en2']
        comp = False
        subj = True
        for item in t:
            if item.lower() not in gen.lower():
                subj = False
        comp_list = ["is a", "is like a", "is an", "is like an", "is the", "is like the", 'like a', 'like the', "is like"]
        for item in comp_list:
            if item in gen:
                comp = True
        if subj and comp:
            succ += 1
            split['metaphor']+=1
    elif "ending in" in src:
        t3 = re.findall("ending in '([^']*)'", src)
        tot_split['end']+=1
        t = t3
        t = list(set(t))
        if len(t) == 0:
            continue
        temp = ""
        found_all = True
        for i in t:
            temp+=i+' '
            if i.lower() not in obj['generation'].lower():
                found_all = False
        temp = obj['generation'].replace(".", "")
        temp = temp.replace(",", "")
        temp = temp.split()
        if found_all and t[0].lower() == temp[-1].lower():
            succ+=1
            split['end']+=1
    elif "starts with" in src:
        tot_split['start']+=1
        t3 = re.findall("starts with the word '([^']*)'", src)
        t = t3
        t = list(set(t))
        if len(t) == 0:
            continue
        temp = ""
        found_all = True
        for i in t:
            temp+=i+' '
            if i.lower() not in obj['generation'].lower():
                found_all = False
        temp = obj['generation'].replace(".", "")
        temp = temp.replace(",", "")
        temp = temp.split()
        if found_all and t[0].lower() == temp[0].lower():
            succ+=1
            split['start']+=1
    else:
        tot_split['subject']+=1
        t = re.findall("about '([^']*)'", src)
        t2 = re.findall("word '([^']*)'", src)
        t3 = re.findall("ending in '([^']*)'", src)
        t4 = re.findall("contains '([^']*)'", src)
        t = t + t2 + t3 +t4
        t = list(set(t))
        if len(t) == 0:
            continue
        temp = ""
        found_all = True
        for i in t:
            temp+=i+' '
            if i.lower() not in obj['generation'].lower():
                found_all = False
        if found_all:
            succ+=1
            split['subject']+=1

print(succ/tot, succ, tot)
print(tot_split, sum([tot_split[k] for k in tot_split.keys()]))
print(split)

"""
"""

import sys
import pronouncing
import json
import re
from datasets import load_metric

filename = sys.argv[1]
eval_type = sys.argv[2]

if eval_type == "subject":
    subj = []
    gen = []

    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['translation']['en1']
            t = re.findall("about '([^']*)'", src)
            t2 = re.findall("word '([^']*)'", src)
            t3 = re.findall("ending in '([^']*)'", src)
            t = t + t2 + t3
            t = list(set(t))
            if len(t) == 0:
                continue
            temp = ""
            for i in t:
                temp+=i+' '
            subj.append(temp)
            gen.append(obj['translation']['en2'])
    
    rouge = load_metric("rouge")
    results = rouge.compute(predictions = gen, references = subj)
    print('Rouge 1', results['rouge1'])
    print('Rouge 2', results['rouge2'])
    print('Rouge L', results['rougeL'])

elif eval_type == "rhyme":
    # gen = []
    tot = 0
    succ = 0
    rhymes = []
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['translation']['en1']
            t = re.findall("rhymes with '([^']*)'", src)
            t = list(set(t))
            if len(t) == 0:
                continue
            #print(t, src)
            src_word = t[0]
            gen = obj['translation']['en2']
            last_word = gen.split()[-1]
            #print(last_word, gen)
            #print(pronouncing.rhymes(src_word))
            flag = False
            for word in pronouncing.rhymes(src_word):
                if last_word in word or word in last_word:
                    # print("Rhymes", last_word, word)
                    succ +=1
                    rhymes.append({'src':src, 'gen':gen, 'last_word':last_word, 'rhyme':word})
                    flag = True
                    break
            # if not flag:
                # print(last_word, src_word, pronouncing.rhymes(src_word), src, gen)
                # ch = input()
            tot+=1

    print("Percentage rhyming: ", float(succ)/tot, tot, succ)
    #ch = input()
elif eval_type == "metaphor":
    succ = 0
    tot = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['translation']['en1']
            if 'metaphor' not in src:
                continue
            t = re.findall("'([^']*)'", src)
            if len(t) == 0:
                continue
            gen = obj['translation']['en2']
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
            tot+=1
            if subj and comp:
                succ += 1
            else:
            #    print(t, src, gen)
                continue
                # ch = input()
    print("Percentage with subject and comparator: ", float(succ)/tot, tot, succ)

elif eval_type == "simile":
    succ = 0
    tot = 0
    comp_ct = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['translation']['en1']
            if 'simile' not in src:
                continue
            t = re.findall("'([^']*)'", src)
            if len(t) == 0:
                continue
            gen = obj['translation']['en2']
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
            tot+=1
            if subj and comp:
                succ += 1
            elif comp:
                comp_ct += 1
            else:
            #    print(t, src, gen)
                continue
                # ch = input()
    print("Percentage with subject and comparator: ", float(succ)/tot, tot, succ)
    print("Percentage with comparator: ", float(comp_ct)/tot, tot, comp_ct)



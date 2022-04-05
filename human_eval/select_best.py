import sys
import pronouncing
import json
import re
import syllapy
import scipy.stats as st
from datasets import load_metric
import random

filename = sys.argv[1]

ip = []
with open(filename, 'r') as f:
    for line in f:
        ip.append(json.loads(line.strip()))

op = []
for item in ip:
    inst = item['instruction']
    if 'simile' in inst:
        src = item['instruction']#'translation']['en1']
        if 'simile' not in src:
            continue
        t = re.findall("'([^']*)'", src)
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
        output = item['output']#'translation']['en2']
        comp = False
        subj = True
        options = []
        options_soft = []
        for gen in output:
            for s_item in t:
                if s_item.lower() not in gen.lower():
                    subj = False

            comp_list = ["is a", "is like a", "is an", "is like an", "is the", "is like the", 'like a', 'like the', "is like"]
            for s_item in comp_list:
                if s_item in gen:
                    comp = True
            if subj and comp:
                options.append(gen)
            if comp or subj:
                options_soft.append(gen)

        # print(options)
        if len(options) > 0:
            sel = random.choice(options)
        elif len(options_soft) > 0:
            sel = random.choice(options_soft)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
        continue
    elif 'metaphor' in inst:
        src = item['instruction']#'translation']['en1']
        if 'metaphor' not in src:
            continue
        t = re.findall("'([^']*)'", src)
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
        # gen = obj['generation']#'translation']['en2']
        output = item['output']#'translation']['en2']
        comp = False
        subj = True
        options = []
        options_soft = []
        for gen in output:
            # print(t, src, gen)
            for s_item in t:
                if s_item.lower() not in gen.lower():
                    subj = False
            comp_list = ["is a", "is like a", "is an", "is like an", "is the", "is like the", 'like a', 'like the', "is like"]
            for s_item in comp_list:
                if s_item in gen:
                    comp = True
            if subj and comp:
                options.append(gen)
            if comp or subj:
                options_soft.append(gen)

        # print(options)
        if len(options) > 0:
            sel = random.choice(options)
        elif len(options_soft) > 0:
            sel = random.choice(options_soft)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
        continue
    elif 'rhym' in inst:
        src = item['instruction'] #translation']['en1']
        t = re.findall("rhymes with '([^']*)'", src)
        t = list(set(t))
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
            #print(t, src)
        src_word = t[0]
        output = item['output'] #translation']['en2']
            #print(last_word, gen)
            #print(pronouncing.rhymes(src_word))
        options = []
        for gen in output:
            flag = False
            last_word = gen.split()[-1]
            for word in pronouncing.rhymes(src_word):
                if last_word in word or word in last_word:
                    # print("Rhymes", last_word, word)
                    options.append(gen)
        # print(options)
        if len(options) > 0:
            sel = random.choice(options)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
        continue
    elif 'haiku' in inst:
        src = item['instruction']#'translation']['en1']
        if 'haiku' not in src:
            continue
        t = re.findall("'([^']*)'", src)
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
        output = item['output']#'translation']['en2']
        options = []
        options_soft = []
        for gen in output:
            subj = True
            exact, close, perfect, near_perfect = False, False, False, False
            for s_item in t:
                if s_item.lower() not in gen.lower():
                    subj = False

            count = 0
            for word in gen.split():
                if word == '/':
                    continue
                count+=syllapy.count(word)
            if count == 17:
                exact=True
            if count >= 12 and count <= 21:
                close=True
            if subj and exact:
                perfect=True
            if subj and close:
                near_perfect=True
            if perfect:
                options.append(gen)
            if near_perfect:
                options_soft.append(gen)
        # print(options)
        # print("soft_options", options_soft)
        if len(options) > 0:
            sel = random.choice(options)
        elif len(options_soft) > 0:
            sel = random.choice(options_soft)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
        continue
    elif "ending" in inst:
        subj = []
        gen = []
        src = item['instruction']
        t3 = re.findall("ending in '([^']*)'", src)
        t = t3
        t = list(set(t))
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
        temp = ""
        options = []
        options_soft = []
        for gen in item['output']:
            found_all = True
            for i in t:
                temp+=i+' '
                if i.lower() not in gen.lower():
                    # print(i, i in obj['generation'], t)
                    found_all = False
            if found_all:
                options_soft.append(gen)
            # print(t, found_all, src, obj['generation'])
            temp = gen.replace(".", "")
            temp = temp.replace(",", "")
            temp = temp.split()
            if t[0].lower() == temp[-1].lower():
                options.append(gen)
        # print(options)
        # print("soft_options", options_soft)
        if len(options) > 0:
            sel = random.choice(options)
        elif len(options_soft) > 0:
            sel = random.choice(options_soft)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
        continue
    elif "start" in inst:
        subj = []
        gen = []
        src = item['instruction']
        t2 = re.findall("starting in '([^']*)'", src)
        t3 = re.findall("starts with the word '([^']*)'", src)
        t = t2 + t3
        t = list(set(t))
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
        temp = ""
        options = []
        options_soft = []
        for gen in item['output']:
            found_all = True
            for i in t:
                temp+=i+' '
                if i.lower() not in gen.lower():
                    # print(i, i in obj['generation'], t)
                    found_all = False
            if found_all:
                options_soft.append(gen)
            # print(t, found_all, src, obj['generation'])
            temp = gen.replace(".", "")
            temp = temp.replace(",", "")
            temp = temp.split()
            if t[0].lower() == temp[0].lower():
                options.append(gen)
        # print(options)
        # print("soft_options", options_soft)
        if len(options) > 0:
            sel = random.choice(options)
        elif len(options_soft) > 0:
            sel = random.choice(options_soft)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
        continue
    else:
        subj = []
        gen = []
        src = item['instruction']
        t = re.findall("about '([^']*)'", src)
        t2 = re.findall("word '([^']*)'", src)
        t3 = re.findall("ending in '([^']*)'", src)
        t4 = re.findall("contains '([^']*)'", src)
        t = t + t2 + t3 +t4
        t = list(set(t))
        # print(src, t)
        if len(t) == 0:
            op_item = {"instruction":inst, "generation":item['generation']}
            op.append(op_item)
            continue
            # print("Proceeding")
        options = []
        options_soft = []
        for gen in item['output']:
            found_all = True
            found_some = False
            for i in t:
                # print(i, i in obj['generation'], t)
                if i.lower() not in item['generation'].lower():
                    # print("Found")
                    found_all = False
                if i.lower() in item['generation'].lower():
                    found_some = True
            # print(t, found_all, src, obj['generation'])
            if found_all:
                options.append(gen)
            if found_some:
                options_soft.append(gen)
        # print(options)
        # print("soft_options", options_soft)
        if len(options) > 0:
            sel = random.choice(options)
        elif len(options_soft) > 0:
            sel = random.choice(options_soft)
        else:
            sel = item['generation']
        # print("Selected ", sel)
        # print("Base ", item)
        op_item = {"instruction":inst, "generation":sel}
        op.append(op_item)
    

with open(filename+".selected", "w") as f:
    for item in op:
        f.write(json.dumps(item)+'\n')

import sys
import pronouncing
import json
import re
import syllapy
import scipy.stats as st
from datasets import load_metric

filename = sys.argv[1]
eval_type = sys.argv[2]

if eval_type == "subject":
    subj = []
    gen = []
    tot = 0
    succ = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction']
            t = re.findall("about '([^']*)'", src)
            t2 = re.findall("word '([^']*)'", src)
            t3 = re.findall("ending in '([^']*)'", src)
            t4 = re.findall("contains '([^']*)'", src)
            t = t + t2 + t3 +t4
            t = list(set(t))
            # print(src, t)
            if len(t) == 0:
                continue
            # print("Proceeding")
            temp = ""
            found_all = True
            for i in t:
                temp+=i+' '
                # print(i, i in obj['generation'], t)
                if i.lower() not in obj['generation'].lower():
                    # print("Found")
                    found_all = False
            # print(t, found_all, src, obj['generation'])
            tot+=1
            if found_all:
                succ+=1
            subj.append(temp)
            gen.append(obj['generation'])
    
    rouge = load_metric("rouge")
    results = rouge.compute(predictions = gen, references = subj)
    print("Total match % ", float(succ)/tot, succ, tot)
    print('Rouge 1', results['rouge1'].mid)
    print('Rouge 2', results['rouge2'].mid)
    print('Rouge L', results['rougeL'].mid)


elif eval_type == "rhyme":
    # gen = []
    tot = 0
    succ = 0
    rhymes = []
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction'] #translation']['en1']
            t = re.findall("rhymes with '([^']*)'", src)
            t = list(set(t))
            if len(t) == 0:
                continue
            #print(t, src)
            src_word = t[0]
            gen = obj['generation'] #translation']['en2']
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

    print("Percentage rhyming: ", float(succ)/tot, succ, tot, tot, succ)
    #ch = input()
elif eval_type == "metaphor":
    succ = 0
    tot = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction']#'translation']['en1']
            if 'metaphor' not in src:
                continue
            t = re.findall("'([^']*)'", src)
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
            tot+=1
            if subj and comp:
                succ += 1
            else:
            #    print(t, src, gen)
                continue
                # ch = input()
    print("Percentage with subject and comparator: ", float(succ)/tot, succ, tot, tot, succ)

elif eval_type == "simile":
    succ = 0
    tot = 0
    comp_ct = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction']#'translation']['en1']
            if 'simile' not in src:
                continue
            t = re.findall("'([^']*)'", src)
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
            tot+=1
            if subj and comp:
                succ += 1
            if comp:
                comp_ct += 1
            else:
            #    print(t, src, gen)
                continue
                # ch = input()
    print("Percentage with subject and comparator: ", float(succ)/tot, succ, tot, tot, succ)
    print("Percentage with comparator: ", float(comp_ct)/tot, tot, comp_ct)

elif eval_type == "haiku":
    exact = 0
    close = 0
    subj_count = 0
    tot = 0
    perfect = 0
    near_perfect = 0
    counts = []
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction']#'translation']['en1']
            if 'haiku' not in src:
                continue
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
            if count == 17:
                exact+=1
            if count >= 15 and count <= 19:
                close+=1
            if subj and count == 17:
                perfect+=1
            if subj and count >= 15 and count <= 19:
                near_perfect+=1
            tot+=1
            counts.append(count)
            # ch = input()
    print("Total: ", tot)
    print("Exactly 17 syllables: ", exact, float(exact)/tot)
    print("Subject + Exactly 17 syllables: ", perfect, float(perfect)/tot)
    print("Between 15 and 19 syllables: ", close, float(close)/tot)
    print("Subject + Between 15 and 19 syllables: ", near_perfect, float(near_perfect)/tot)

    stat = st.binned_statistic(counts, counts, bins = 10, statistic = 'count')
    print(stat)
elif eval_type == "ending":
    subj = []
    gen = []
    tot = 0
    succ = 0
    ending = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction']
            t3 = re.findall("ending in '([^']*)'", src)
            t = t3
            t = list(set(t))
            if len(t) == 0:
                continue
            temp = ""
            found_all = True
            for i in t:
                temp+=i+' '
                if i.lower() not in obj['generation'].lower():
                    # print(i, i in obj['generation'], t)
                    found_all = False
            # print(t, found_all, src, obj['generation'])
            tot+=1
            if found_all:
                succ+=1
            temp = obj['generation'].replace(".", "")
            temp = temp.replace(",", "")
            temp = temp.split()
            if t[0].lower() == temp[-1].lower():
                ending+=1
            # else:
            #    print("Failed End Test")
            subj.append(temp)
            gen.append(obj['generation'])
    
    rouge = load_metric("rouge")
    results = rouge.compute(predictions = gen, references = subj)
    print("Total match accuracy: ", float(succ)/tot, succ, tot)
    print("Total end accuracy: ", float(ending)/tot)
    print('Rouge 1', results['rouge1'].mid)
    print('Rouge 2', results['rouge2'].mid)
    print('Rouge L', results['rougeL'].mid)

elif eval_type == "starting":
    subj = []
    gen = []
    tot = 0
    succ = 0
    starting = 0
    with open(filename, 'r') as f:
        for line in f:
            obj = json.loads(line.strip())
            src = obj['instruction']
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
                    # print(i, i in obj['generation'], t)
                    found_all = False
            tot+=1
            if found_all:
                succ+=1
            # print(t, found_all, src, obj['generation'])
            temp = obj['generation'].replace(".", "")
            temp = temp.replace(",", "")
            temp = temp.split()
            if t[0].lower() == temp[0].lower():
                starting+=1
            # else:
            #    print("Failed Start Test")
            subj.append(temp)
            gen.append(obj['generation'])
    
    rouge = load_metric("rouge")
    results = rouge.compute(predictions = gen, references = subj)
    print("Total match accuracy: ", float(succ)/tot, succ, tot)
    print("Total start accuracy: ", float(starting)/tot)
    print('Rouge 1', results['rouge1'].mid)
    print('Rouge 2', results['rouge2'].mid)
    print('Rouge L', results['rougeL'].mid)


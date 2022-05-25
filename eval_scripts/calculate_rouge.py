from rouge_score import rouge_scorer
import ast
import sys
import json

with open(sys.argv[1], 'r') as f:
    obj = json.loads(f.read())
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
poem = obj['poemsofar']
insts = ' '.join([' '.join(item['output']) for item in ast.literal_eval(obj['logs'])])
#print(insts)
#print(poem)
#for line in poem.split("\r\n"):
#    print(line, line in insts)
scores = scorer.score(poem, insts)#insts, poem)
print(scores)

import sys
import json
import torch
import copy
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM

val_fname = sys.argv[1]
model_path = sys.argv[2]

print("Running generation for model at: ", model_path, " on filename: ", val_fname)

ip = []
with open(val_fname, 'r') as f:
    for line in f:
        ip.append(json.loads(line.strip()))

print(len(ip))

config = AutoConfig.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
print(config)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, cache_dir="./temp/")
model = model.to('cuda')

# instruction = "translate English to German: How are you doing today?"
op = []
for item in ip:
    instruction = item['translation']['en1']
    inputs = tokenizer(instruction, return_tensors="pt").input_ids
    # sample_outputs = model.generate(input_ids=inputs.to('cuda'), no_repeat_ngram_size=2, do_sample=True, max_length=64, top_k=5,temperature=0.7,early_stopping=True,eos_token_id=tokenizer.eos_token_id)
    outputs = model.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, do_sample=True, max_length=50, top_k=5, temperature=0.7, early_stopping=True, eos_token_id= tokenizer.eos_token_id)
    output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # print(output)#.split('.')[0]
    op_item = copy.deepcopy(item)
    op_item['generation'] = output
    op_item['instruction'] = instruction
    op.append(op_item)

print(len(op))

with open("with-gen-"+val_fname, "w") as f:
    for item in op:
        f.write(json.dumps(item)+'\n')




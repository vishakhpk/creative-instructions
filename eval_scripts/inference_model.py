import sys
import json
import copy
import pickle
from transformers import AutoConfig, AutoTokenizer, AutoModelForSeq2SeqLM

model_path = sys.argv[1]
input_file = sys.argv[2] 
output_file = sys.argv[3] 

print(model_path, input_file, output_file)

config = AutoConfig.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to('cuda')
if "11B" in model_path:
    model.parallelize()

ip = []
with open(input_file, 'r') as f:
    for line in f:
        ip.append(json.loads(line.strip()))

op = []
for item in ip:
    # instruction = "Write a poetic sentence that ends in a word which rhymes with 'kill'"
    instruction = item['translation']['en1']
    inputs = tokenizer(instruction, return_tensors="pt").input_ids
    sample_outputs = model.generate(input_ids=inputs.to('cuda'), do_sample=True, max_length=128, top_k=5,temperature=0.7, eos_token_id=tokenizer.eos_token_id, num_return_sequences = 5)
    output = tokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
    # print(output)#.split('.')[0]
    op_item = copy.deepcopy(item)
    op_item['output'] = output
    op_item['instruction'] = instruction
    op_item['generation'] = output[0]
    op.append(op_item)

    

# pickle.dump(op, open(output_file, 'wb'))
with open(output_file, "w") as f:
    for item in op:
        f.write(json.dumps(item)+'\n')

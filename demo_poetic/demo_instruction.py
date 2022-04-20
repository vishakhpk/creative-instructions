from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM, T5ForConditionalGeneration
import os, sys,random
import yake
import ast
import pronouncing
from wordfreq import zipf_frequency
import re
import sys
import torch
import json
import spacy
os.environ["CUDA_VISIBLE_DEVICES"]="0,1"

import numpy as np
app = Flask(__name__)
CORS(app)
instructionmodel = None
instructiontokenizer = None
nlp = None

@app.route("/", methods=["GET", "POST"])
@cross_origin(origin="*")
def home():
	if (request.method == "POST"):
		form = request.form
		print(request.form)
		if ('poem_submit' in form) and form["poem_submit"] == "poem_submit":
	                print("Submitting Poem")
	                with open(form["uid"]+".json", "w") as f:
	                    f.write(json.dumps(form))
	                return render_template("index1.html", f='')
		topic = None # form["topic"]
		startword = None # form["startword"]
		endword = None # form["endword"]
		lang = form["inst"]
		print("LANG isss",lang)
		rhymewithword = form["rhymewithword"]
		nl_inst = form["nlinstruction"]
		if nl_inst == "Hit the button above to edit your instruction in text":
			nl_inst = None
		if "poemsofar" in form:
			poem_lines = form["poemsofar"].split('\n')
		else:
			poem_lines =  [] # ['a', 'b']
		translation = get_translation(topic, startword, endword, rhymewithword, lang, poem_lines, nl_inst)
		if ('logs' not in form):
	                logs = []
		else:
	                logs = ast.literal_eval(form['logs'])
		logs.append({'instruction':nl_inst, 'output':translation}) 
		if ('poemtitle' not in form):
	                poemtitle=''
		else:
	                poemtitle=form['poemtitle']
		# return render_template("instruction.html", poem=poem_lines, translation=get_translation(topic, startword, endword, rhymewithword, lang, poem_lines, nl_inst), instruction=nl_inst)
		return render_template("instruction.html", poem=poem_lines, translation=translation, instruction=nl_inst, logs=logs, poemtitle=poemtitle)

	return render_template("index1.html", f='')

def get_translation(topic, startword, endword, rhymewithword, lang, poemsofar, nl_inst):
	print("NLinst",nl_inst)
	# return ["a", "b", "c", "d", "e"]
	if (nl_inst is not None) and (lang not in ['endwithrhyme','comp3','comp4','suggesttopic']):
		instruction = nl_inst
		print("I AM HERE......")
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 10, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		output.sort(key=len,reverse=True)
		return output[0:5]
	if lang=="suggesttopic":
		inputs = instructiontokenizer(nl_inst, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		arr = []
		for elem in output:
			keywords = kw_extractor.extract_keywords(elem)
			arr.append(keywords[0][0])
		return arr
	if lang=="endwithrhyme":
		last_word = nl_inst.replace("'",'').split('ending in a rhyme for ')[1].rstrip()
		x = [(zipf_frequency(elem,'en'),elem) for elem in pronouncing.rhymes(last_word) if len(elem)>=3 and zipf_frequency(elem,'en')>=3.0 and '.' not in elem and '-' not in elem]
		x = sorted(x,reverse=True)
		arr = []
		for i in range(0,min(15,len(x))):
			tokens = nlp(last_word+' '+x[i][1])
			sim = tokens[0].similarity(tokens[1])
			arr.append((sim,x[i][1]))
		arr = sorted(arr,reverse=True)
		print("Topic is ",topic)
		inst = []
		for i in range(0,min(5,len(arr))):
			last_word = arr[i][1]
			instruction = random.choice(["Write a poetic sentence ending in '"+last_word+"'","Generate a poetic sentence ending in '"+last_word+"'"])
			inst.append(instruction)
			inst.append(instruction)
		while len(inst)<10:
			inst.append(instruction)
		print(inst)
		inputs = instructiontokenizer(inst, padding=True,return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 10, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		output.sort(key=len,reverse=True)
		return output[0:5]
		return output
	if lang=='comp3':
		last_word = nl_inst.replace("'",'').split('ending in a rhyme for ')[1].rstrip()
		topic = nl_inst.replace("'",'').split('Write a poetic sentence that contains the word ')[1].split(' and ending')[0]
		x = [(zipf_frequency(elem,'en'),elem) for elem in pronouncing.rhymes(last_word) if len(elem)>=3 and zipf_frequency(elem,'en')>=3.0 and '.' not in elem and '-' not in elem]
		x = sorted(x,reverse=True)
		arr = []
		for i in range(0,min(15,len(x))):
			tokens = nlp(last_word+' '+x[i][1])
			sim = tokens[0].similarity(tokens[1])
			arr.append((sim,x[i][1]))
		arr = sorted(arr,reverse=True)
		print("Topic is ",topic)
		inst = []
		for i in range(0,min(5,len(arr))):
			last_word = arr[i][1]
			instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence that includes the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence about '"+topic+"' and ending in '"+last_word+"'"])
			inst.append(instruction)
			inst.append(instruction)
		while len(inst)<10:
			inst.append(inst[-1])
		print(inst)
		inputs = instructiontokenizer(inst, padding=True, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 10, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		output.sort(key=len,reverse=True)
		return output[0:5]
		return output
	if lang=='comp4':
		rhymewithword = nl_inst.replace("'",'').split('ending in a rhyme for ')[1].rstrip()
		topic = nl_inst.replace("'",'').split('Write a poetic sentence that contains the word ')[1].split(' and ending')[0]
		x = [(zipf_frequency(elem,'en'),elem) for elem in pronouncing.rhymes(rhymewithword) if len(elem)>=3 and zipf_frequency(elem,'en')>=3.0 and '.' not in elem and '-' not in elem]
		x = sorted(x,reverse=True)
		arr = []
		last_word = ''
		for i in range(0,min(15,len(x))):
			tokens = nlp(rhymewithword+' '+x[i][1])
			sim = tokens[0].similarity(tokens[1])
			arr.append((sim,x[i][1]))
		arr = sorted(arr,reverse=True)
		inst = []
		for i in range(0,min(5,len(arr))):
			last_word = arr[i][1]
			instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence that includes the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence about '"+topic+"' and ending in '"+last_word+"'"])
			inst.append(instruction)
			inst.append(instruction)
		print(inst,len(inst))
		while len(inst)<10:
			inst.append(inst[-1])
		inputs = instructiontokenizer(inst, padding=True,return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 1, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		output.sort(key=len,reverse=True)
		return output[0:5]

if __name__ == '__main__':
	model_dir = "/mnt/nlp_swordfish/tuhin/poetryT511bcheckpoints/epoch3"
	try: 
		instructiontokenizer = AutoTokenizer.from_pretrained(model_dir)
	except:
		model_dir = sys.argv[1] 
		instructiontokenizer = AutoTokenizer.from_pretrained(model_dir)
	instructionmodel = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
	kw_extractor = yake.KeywordExtractor(n=3)
	print("Loaded......")
	if torch.cuda.is_available() and torch.cuda.device_count() > 1:
		instructionmodel.parallelize()
		nlp = spacy.load('en_core_web_md')
	app.run(host='0.0.0.0',port=8056, debug=False)

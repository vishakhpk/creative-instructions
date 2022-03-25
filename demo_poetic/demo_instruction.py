from flask import Flask, request, render_template
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM, T5ForConditionalGeneration
import os, sys,random
import yake
import pronouncing
import re
import sys
import torch

os.environ["CUDA_VISIBLE_DEVICES"]="2,3"
import numpy as np
app = Flask(__name__)
instructionmodel = None
instructiontokenizer = None

@app.route("/", methods=["GET", "POST"])
def home():
	if (request.method == "POST"):
		form = request.form
		topic = form["topic"]
		startword = form["startword"]
		endword = form["endword"]
		lang = form["lang"]
		rhymewithword = None # form["rhymewithword"]
		nl_inst = form["nlinstruction"]
		if nl_inst == "Hit the button above to edit your instruction in text":
			nl_inst = None
		if "poemsofar" in form:
			poem_lines = form["poemsofar"].split('\n')
		else:
			poem_lines =  []
			# poem_lines =  ["q", "w", "e"]
		return render_template("instruction.html", poem=poem_lines, translation=get_translation(topic, startword, endword, rhymewithword, lang, poem_lines, nl_inst))

	return render_template("index1.html", f='')

def get_translation(topic, startword, endword, rhymewithword, lang, poemsofar, nl_inst):
	if nl_inst is not None:
		instruction = nl_inst
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		# output = ["a", "b", "c", "d", "e"]
		return output
	if lang=="about":
		print("Topic is ",topic)
		instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"'", "Write a poetic sentence that includes the word '"+topic+"'", "Write a poetic sentence about '"+topic+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		# output = ["a", "b", "c", "d", "e"]
		return output
	elif lang=="suggest":
		last_sentence = poemsofar[-1]
		instruction = random.choice(["Write a next sentence in a poetry given the previous sentence '"+last_sentence+"'","Generate a next sentence in a poetry given the previous sentence '"+last_sentence+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=="suggesttopic":
		last_sentence = poemsofar[-1]
		instruction = random.choice(["Write a next sentence in a poetry given the previous sentence '"+last_sentence+"'","Generate a next sentence in a poetry given the previous sentence '"+last_sentence+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		arr = []
		for elem in output:
			keywords = kw_extractor.extract_keywords(elem)
			arr.append(keywords[0][0])
		return arr
	elif lang=="endwithaword":
		print("End word is ",endword)
		instruction = random.choice(["Write a poetic sentence ending in '"+endword+"'","Generate a poetic sentence ending in '"+endword+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=="startwithaword":
		print("Start word is ",startword)
		startword = startword.capitalize()
		instruction = random.choice(["Write a poetic sentence that starts with the word '"+startword+"'","Generate a poetic sentence that starts with the word '"+startword+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=="endwithrhyme":
		last_sentence = re.sub(r'[^\w\s]', '', poemsofar[-1])
		last_word = last_sentence.split()[-1]
		last_word = random.choice(pronouncing.rhymes(last_word)[0:3])
		instruction = random.choice(["Write a poetic sentence ending in '"+last_word+"'","Generate a poetic sentence ending in '"+last_word+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=='comp1':
		print("Topic is ",topic)
		instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"' and ending in '"+endword+"'", "Write a poetic sentence that includes the word '"+topic+"' and ending in '"+endword+"'", "Write a poetic sentence about '"+topic+"' and ending in '"+endword+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=='comp2':
		startword = startword.capitalize()
		instruction = random.choice(["Write a poetic sentence that starts with the word '"+startword+"' and ending in '"+endword+"'", "Generate a poetic sentence that starts with the word '"+startword+"' and ending in '"+endword+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=='comp3':
		last_sentence = re.sub(r'[^\w\s]', '', poemsofar[-1])
		last_word = last_sentence.split()[-1]
		last_word = random.choice(pronouncing.rhymes(last_word)[0:3])
		print("Topic is ",topic)
		instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence that includes the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence about '"+topic+"' and ending in '"+last_word+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output
	elif lang=='comp4':
		last_word = random.choice(pronouncing.rhymes(rhymewithword)[0:3])
		print("Topic is ",topic)
		instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence that includes the word '"+topic+"' and ending in '"+last_word+"'", "Write a poetic sentence about '"+topic+"' and ending in '"+last_word+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output

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
	app.run(host='0.0.0.0',port=8056, debug=False)

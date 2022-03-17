from flask import Flask, request, render_template
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM, T5ForConditionalGeneration
import os, sys,random
import yake
import re

os.environ["CUDA_VISIBLE_DEVICES"]="0,1"
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
		if "poemsofar" in form:
			poem_lines = form["poemsofar"].split('\n')
		else:
			poem_lines = []
		return render_template("instruction.html", poem=poem_lines, translation=get_translation(topic,startword,endword,lang,poem_lines))

	return render_template("index1.html", f='')

def get_translation(topic,startword,endword,lang,poemsofar):
	if lang=="about":
		print("Topic is ",topic)
		instruction = random.choice(["Write a poetic sentence that contains the word '"+topic+"'", "Write a poetic sentence that includes the word '"+topic+"'", "Write a poetic sentence about '"+topic+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
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
		instruction = random.choice(["Write a poetic sentence that ends in a word which rhymes with '"+last_word+"'","Generate a poetic sentence that ends in a word which rhymes with '"+last_word+"'"])
		print(instruction)
		inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
		sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
		output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
		return output

if __name__ == '__main__':
	instructiontokenizer = AutoTokenizer.from_pretrained("/mnt/nlp_swordfish/tuhin/poetryT511bcheckpoints/epoch3") 
	instructionmodel = AutoModelForSeq2SeqLM.from_pretrained("/mnt/nlp_swordfish/tuhin/poetryT511bcheckpoints/epoch3")
	kw_extractor = yake.KeywordExtractor(n=3)
	print("Loaded......")
	instructionmodel.parallelize()
	app.run(host='0.0.0.0',port=8056, debug=False)

from flask import Flask, request, render_template
from transformers import MBartForConditionalGeneration, MBart50Tokenizer
import os, sys
os.environ["CUDA_VISIBLE_DEVICES"]="1"
import numpy as np
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
	if (request.method == "POST"):
		form = request.form
		poem = form["poem"]
		lang = form["lang"]
		model_name = form["model"]
		poem_lines = poem.split('\n')
		return render_template("translation.html", poem=poem_lines, translation=get_transaltion(poem_lines, lang, model_name))

	return render_template("index.html", f='')

def get_transaltion(poem_lines, lang, model_name):
	trans_lines = []
	for line in poem_lines:
		trans_lines.append(translate(line, lang, model_name))
	return trans_lines 

def translate(src, src_lang, model_name):

	if model_name=='mbart-50':
		model = mbart50_model
		tokenizer = mbart50_tokenizer

	elif src_lang[:3]+model_name=='ru_poetic_all':
		model = ru_poetic_all_model
		tokenizer = ru_poetic_all_tokenizer

	elif src_lang[:3]+model_name=='pt_poetic_all':
		model = pt_poetic_all_model
		tokenizer = pt_poetic_all_tokenizer

	elif src_lang[:3]+model_name=='nl_poetic_all':
		model = de_poetic_all_model
		tokenizer = de_poetic_all_tokenizer
	elif src_lang[:3]+model_name=='de_poetic_all':
		model = nl_poetic_all_model
		tokenizer = nl_poetic_all_tokenizer

	elif src_lang[:3]+model_name=='es_poetic_all':
		model = rom_poetic_all_model
		tokenizer = rom_poetic_all_tokenizer
	elif src_lang[:3]+model_name=='it_poetic_all':
		model = rom_poetic_all_model
		tokenizer = rom_poetic_all_tokenizer
		
	else: return "Model name invalid" 

	model.eval()
	model.to('cuda')
	tokenizer.src_lang = src_lang
	inputs = tokenizer(src, return_tensors="pt")
	inputs = inputs.to('cuda')
	generated_tokens = model.generate(**inputs, no_repeat_ngram_size=2, num_beams=5,num_return_sequences=5,forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
	res = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
	res = [(r,len(r.split())) for r in res]
	return res[0][0]

if __name__ == '__main__':

	
	
	print("Loading German poetic model")
	de_poetic_all_tokenizer = MBart50Tokenizer.from_pretrained("TuhinColumbia/germanpoetrymany")
	de_poetic_all_model = MBartForConditionalGeneration.from_pretrained("TuhinColumbia/germanpoetrymany")


	print("Loading Portuguese poetic model")
	pt_poetic_all_tokenizer = MBart50Tokenizer.from_pretrained("TuhinColumbia/portugesepoetrymany")
	pt_poetic_all_model = MBartForConditionalGeneration.from_pretrained("TuhinColumbia/portugesepoetrymany")

	print("Loading Russian poetic model")
	ru_poetic_all_tokenizer = MBart50Tokenizer.from_pretrained("TuhinColumbia/russianpoetrymany")
	ru_poetic_all_model = MBartForConditionalGeneration.from_pretrained("TuhinColumbia/russianpoetrymany")


	print("Loading Romance poetic model")
	rom_poetic_all_tokenizer = MBart50Tokenizer.from_pretrained("TuhinColumbia/romancelanguagepoetry")
	rom_poetic_all_model = MBartForConditionalGeneration.from_pretrained("TuhinColumbia/romancelanguagepoetry")

	print("Loading mBART model")
	mbart50_model =  MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")
	mbart50_tokenizer = MBart50Tokenizer.from_pretrained("facebook/mbart-large-50-many-to-one-mmt")

	app.run(host='0.0.0.0',port=8000, debug=False)

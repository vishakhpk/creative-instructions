from flask import Flask, request, render_template
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM, T5ForConditionalGeneration
import os, sys,random
os.environ["CUDA_VISIBLE_DEVICES"]="0,1"
import numpy as np
app = Flask(__name__)
instructionmodel = None
instructiontokenizer = None

@app.route("/", methods=["GET", "POST"])
def home():
	if (request.method == "POST"):
		form = request.form
		instruction = form["poem"]
		poem_lines = [instruction]
		return render_template("instruction.html", poem=poem_lines, translation=get_transaltion(instruction))

	return render_template("index1.html", f='')

def get_transaltion(instruction):
	print("Instruction is",instruction)
	inputs = instructiontokenizer(instruction, return_tensors="pt").input_ids
	print("inputs: ",inputs)
	sample_outputs = instructionmodel.generate(input_ids=inputs.cuda(), no_repeat_ngram_size=2, num_return_sequences = 5, do_sample=True, max_length=64, top_k=5,temperature=0.7,eos_token_id=instructiontokenizer.eos_token_id)
	output = instructiontokenizer.batch_decode(sample_outputs, skip_special_tokens=True)
	print("inputs: ",output)
	res = ""
	for elem in output:
		res = res+elem+"\n"
	return res.rstrip()



if __name__ == '__main__':
	instructiontokenizer = AutoTokenizer.from_pretrained("/mnt/nlp_swordfish/tuhin/poetryT511bcheckpoints/epoch3") 
	instructionmodel = AutoModelForSeq2SeqLM.from_pretrained("/mnt/nlp_swordfish/tuhin/poetryT511bcheckpoints/epoch3")
	print("Loaded......")
	instructionmodel.parallelize()
	app.run(host='0.0.0.0',port=8056, debug=False)

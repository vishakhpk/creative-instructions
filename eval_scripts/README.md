# Evaluation Scripts

## Creative Instructions

### OpenAI InstructGPT
First ensure that you're API key with OpenAI is exported as an environment variable as:
```
export OPENAI_API_KEY={your key here}
```
Then access the API as:
```
python inference_openai_api.py <prompt filename> <filename with instructions> <output filename>
```


### Automatic Eval On Validation Data
First run the generation script:
```
python generate_output.py <filename with instructions i.e. val.json> <stored directory of model>
```
This creates a new jsonl file with stored generations along with the instructions. Proceed to automatic eval. 

Currently tests for subject (rouge match), rhyme (with a dictionary i.e. not perect), haikus (subject and syllable count), simile and metaphor (with templates)
```
python automatic_eval.py <filename with instructions and stored generations> <type of eval: rhyme/subejct/simile/metaphor/haiku>
```

### Run Generation for Human Evaluation
```
python inference_model.py <model directory> <input test set file> <output filename to be written>
```


## SCAN

### Accuracy of generations

```
python eval_accuracy.py <filename of generations from generate_output>
```

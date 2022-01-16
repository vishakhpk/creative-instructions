# Evaluation Scripts

## Automatic Eval
First run the generation script:
```
python generate_output.py <filename with instructions i.e. val.json> <stored directory of model>
```
This creates a new jsonl file with stored generations along with the instructions. Proceed to automatic eval. 

Currently tests for subject (rouge match), rhyme (with a dictionary i.e. not perect), simile and metaphor (with templates)
```
python automatic_eval.py <filename with instructions and stored generations> <type of eval: rhyme/subejct/simile/metaphor>
```

## TODOs
1. More precise automatic eval
2. Design/HTML for human eval
3. Code to generate test sets

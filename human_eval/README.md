Scripts for Human Evaluation on AMT:

First run inference on any of the trained models with eval\_scripts/inference\_model.py or GPT3 (with eval\_scripts/inference\_openai\_api.py). Then we select the best output using our automatic metrics:

```
python3 select_best.py <filename>
```

Then we create the CSV to be consumed by AMT

```
python3 create_csv.py <t5 output> <gpt3 output> <csv filename>
```

And to analyze the AMT results
```
python3 analyze_batchl
```

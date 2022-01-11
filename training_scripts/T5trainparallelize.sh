export BS=4;
PYTHONPATH=../../../src
USE_TF=0

python ./run_translation1.py \
	--model_name_or_path bigscience/T0_3B \
	--output_dir /local/nlp/temp/3B.rehearsal1000.gigaword \
	--evaluation_strategy=steps \
	--save_strategy=steps \
	--eval_steps 20 \
	--save_steps 20 \
	--do_train \
	--do_eval \
	--train_file /home/tuhin.chakr/gpt3/gigaword/train.gigaword.continual1000.json \
	--validation_file /home/tuhin.chakr/gpt3/gigaword/validation.gigaword.continual1000.json \
	--adafactor \
	--learning_rate 1e-3 \
	--overwrite_output_dir \
	--max_source_length 1024 \
	--max_target_length 256 \
	--num_train_epochs 1 \
	--gradient_accumulation_steps 256 \
	--per_device_train_batch_size $BS \
	--per_device_eval_batch_size $BS \
	--source_lang en_XX \
	--target_lang en_XX
	#--deepspeed /home/tuhin.chakr/gpt3/transformers/tests/deepspeed/ds_config_zero3_adafactor.json 

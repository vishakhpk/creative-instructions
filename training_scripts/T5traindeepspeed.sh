export BS=12; 
PYTHONPATH=../../../src
USE_TF=0

deepspeed --num_gpus=4 ./run_translation.py \
	--model_name_or_path  /local/nlp/temp/poetryT511B0/checkpoint-801 \
	--output_dir /local/nlp/temp/poetryT511B1 \
	--evaluation_strategy=steps \
	--save_strategy=steps \
	--eval_steps 400 \
	--save_steps 400 \
	--do_train \
	--do_eval \
	--train_file /home/tuhin.chakr/gpt3/poetrynew/train.json \
	--validation_file /home/tuhin.chakr/gpt3/poetrynew/val.json \
	--learning_rate 1e-3 \
	--gradient_accumulation_steps 21 \
	--overwrite_output_dir \
	--max_source_length 64 \
	--max_target_length 64 \
	--num_train_epochs 1 \
	--per_device_train_batch_size $BS \
	--per_device_eval_batch_size $BS \
	--source_lang en_XX \
	--target_lang en_XX \
	--deepspeed /home/tuhin.chakr/gpt3/transformers/tests/deepspeed/ds_config_zero3_1.json 

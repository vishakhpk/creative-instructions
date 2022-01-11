export BS=4;
PYTHONPATH=../../../src
USE_TF=0

python ./run_translation_parallelize.py \
	--model_name_or_path t5-3b \
	--output_dir /output/ \
	--evaluation_strategy=epoch \
	--save_strategy=epoch \
	--do_train \
	--do_eval \
	--train_file /home/tuhin.chakr/train.json \
	--validation_file /home/tuhin.chakr/validation.json \
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

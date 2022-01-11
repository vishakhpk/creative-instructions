# Scripts to train model


Name: transformers
Version: 4.13.0.dev0

Name: deepspeed
Version: 0.5.8+09260b6

          git clone https://github.com/huggingface/transformers.git
          cp run_translation_deepspeed.py transformers/examples/pytorch/translation/
          cp run_translation_parallelize.py transformers/examples/pytorch/translation/
          cp T5traindeepspeed.sh transformers/examples/pytorch/translation/
          cp T5trainparallelize.sh transformers/examples/pytorch/translation/
          cp ds_config_zero3_1.json transformers/tests/deepspeed/
          


- Change cache_dir to where you wanna load your pretrained checkpoint in run_translation files
- Advised to run on 4 A100 GPUs 
- If you run on lesser gpu edit following code , remember T5 3B/11B has 24 attention heads and its advised to spread it evenly across gpus for model.parallelize()

          device_ids = [0,1,2,3]
          device_map = {device_ids[0]: list(range(0, 6)),device_ids[1]: list(range(6,12)),device_ids[2]: list(range(12,18)),device_ids[3]: list(range(18,24))}
          model.parallelize(device_map)

## TODOs
1. Deepspeed config + HF code
2. Version/Environment Info
3. Links to checkpoints

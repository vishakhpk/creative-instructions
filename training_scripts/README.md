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

## TODOs
1. Deepspeed config + HF code
2. Version/Environment Info
3. Links to checkpoints

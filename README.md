# Help me write a poem: Instruction Tuning as a Vehicle for Collaborative Poetry Writing

Repo associated with the EMNLP 2022 paper (https://arxiv.org/pdf/2210.13669.pdf)

## Code
- Scripts to train the model with both deepspeed and model parallelism are in training\_scripts with an associated README.  
- Once the models were trained we run automatic evaluation, comparing to pretrained models (T0 3B/ T0pp) and InstructGPT (via the OpenAI API), as directed by the README in eval\_scripts/. We report success rates of models satisfying instructions, averaged over 5 runs. 
- Subsequently, we also perform human evaluation comparing outputs from our finetuned T5-11B model and InstructGPT as seen in human\_eval/.
- Finally we run a user study using the interface in demo\_poetic/. Logs of all user interactions are provided in human\_eval/poems\_submissions

## Data 
- [Drive Link](https://drive.google.com/drive/folders/1TRuo-1wQOKBvMyaitRAMzgTmv9PVFDaH?usp=sharing) to the training and validation data in the instruction format along with the test sets used in the paper.
- [Model generations](https://drive.google.com/drive/folders/1LWQsycZqrJvl1c7HGtJ1aJ-Lu59h8FSR?usp=sharing) used in the paper for automatic evaluation.
- [Poems and user interactions](https://drive.google.com/drive/folders/1qdDa2fGp3_agFRCjeKa61SQvBu8WVyf_?usp=sharing) in the collaborative user study we ran with CoPoet.
- [Model weights](https://drive.google.com/drive/folders/1mjTji9wCfX4KA039wpyQLSMx2A9jLCwe?usp=sharing) of our finetuned T5-11B model (TODO)

## Citation

                                  @article{chakrabarty2022help,
                                    title={Help me write a poem: Instruction Tuning as a Vehicle for Collaborative Poetry Writing},
                                    author={Chakrabarty, Tuhin and Padmakumar, Vishakh and He, He},
                                    journal={arXiv preprint arXiv:2210.13669},
                                    year={2022}
                                  }

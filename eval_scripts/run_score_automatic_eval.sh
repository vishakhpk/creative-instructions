for model in InstructGPT ZeroShot-InstructGPT T53B T03B T0pp T511B_DS 
do
    for subset in ki_ke #ki_ue compositional
    do 
	for idx in 1 2 3 4 5
	do
		echo "----------------------------------------"
		echo $model $subset $idx
		echo "----------------------------------------"
		python3 score_automatic_eval.py outputs/${model}/${subset}_${idx}.output
	done
    done       
done

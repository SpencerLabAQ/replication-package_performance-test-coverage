#!/bin/bash

cd code

echo "Starting fine-tuning with graphcodebert-base..."
echo "Start Time: $(date)"
echo "Logging to: ../logs/train.log"
echo "--------------------------------------------"

python3 run.py \
	--output_dir=../saved_models/graph-codebert-finetuned \
	--model_type=roberta \
	--tokenizer_name=microsoft/graphcodebert-base \
	--model_name_or_path=microsoft/graphcodebert-base \
	--do_train \
	--train_data_file=../data/train.jsonl \
	--eval_data_file=../data/val.jsonl \
	--test_data_file=../data/test.jsonl \
	--epoch 5 \
	--block_size 400 \
	--train_batch_size 16 \
	--eval_batch_size 64 \
	--learning_rate 2e-5 \
	--max_grad_norm 1.0 \
	--evaluate_during_training \
	--seed 123456 2>&1 | tee ../logs/train.log

echo "Training finished at: $(date)"

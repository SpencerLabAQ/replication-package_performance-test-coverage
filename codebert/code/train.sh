#!/bin/bash

echo "🚀 Starting fine-tuning with CodeBERT..."
echo "📅 Start Time: $(date)"
echo "📂 Logging to: ../logs/train.log"
echo "--------------------------------------------"

python3 /NFSHOME/mimran/codebert/code/run.py \
	--output_dir=../saved_models/codebert-finetuned \
	--model_type=roberta \
	--tokenizer_name=microsoft/codebert-base \
	--model_name_or_path=microsoft/codebert-base \
	--do_train \
	--do_eval \
	--do_test \
	--train_data_file=/NFSHOME/mimran/codebert/data/train.jsonl \
	--eval_data_file=/NFSHOME/mimran/codebert/data/val.jsonl \
	--test_data_file=/NFSHOME/mimran/codebert/data/test.jsonl \
	--epoch 5 \
	--block_size 400 \
	--train_batch_size 16 \
	--eval_batch_size 64 \
	--learning_rate 2e-5 \
	--max_grad_norm 1.0 \
	--evaluate_during_training \
	--seed 123456 2>&1 | tee /NFSHOME/mimran/codebert/logs/train.log

echo "✅ Training finished at: $(date)"

#!/bin/bash

if [ ! -d data/kanji_png_128 ]; then
  echo "Please copy your 128x128 PNGs to data/kanji_png_128/"
  exit 1
fi
if [ ! -f data/metadata.jsonl ]; then
  echo "Please copy your metadata.jsonl to data/"
  exit 1
fi

# Ensure metadata.jsonl uses 'image' as the key
sed -i 's/"image":/"file_name":/g' data/metadata.jsonl

accelerate launch train_text_to_image.py \
  --pretrained_model_name_or_path="CompVis/stable-diffusion-v1-4" \
  --dataset_name imagefolder \
  --train_data_dir="data/kanji_png_128" \
  --output_dir="sd_pretrained_output" \
  --resolution=128 \
  --train_batch_size=16 \
  --max_train_steps=20000 \
  --checkpointing_steps=5000 \
  --learning_rate=1e-4 \
  --seed=42 \
 # --from_scratch # This flag indicates training from scratch

echo "SD training complete! Check sd_scratch_output/ for weights."
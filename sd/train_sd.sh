#!/bin/bash

echo "Expected directory structure:"
echo "data/"
echo "  ├── kanji_png_128/ or kanji_png_256/   # Place your PNG images here"
echo "  └── metadata.jsonl                     # Place your metadata file here"

# Ensure metadata.jsonl uses 'image' as the key

echo "To train from scratch, uncomment the --from_scratch flag in the accelerate command below."
echo "Please verify and update the 'train_data_dir' and 'output_dir' variables below as needed for your training setup."

sed -i 's/"image":/"file_name":/g' data/metadata.jsonl

accelerate launch train_text_to_image.py \
  --pretrained_model_name_or_path="CompVis/stable-diffusion-v1-4" \
  --dataset_name imagefolder \
  --train_data_dir="data/kanji_png_128" \
  --output_dir="sd_pretrained_output" \
  --resolution=512 \
  --train_batch_size=16 \
  --max_train_steps=20000 \
  --checkpointing_steps=5000 \
  --learning_rate=1e-4 \
  --seed=42 \
 # --from_scratch # This flag indicates training from scratch

echo "SD training complete! Check sd_scratch_output/ for weights."
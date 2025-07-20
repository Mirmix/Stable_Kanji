#!/bin/bash

# Environment: activate your conda env and install requirements first!

# Prepare data if missing
if [ ! -d text_to_image_data ]; then
  echo "text_to_image_data/ not found. Copying data from ../data/kanji_png_256/ and ../data/metadata.jsonl..."
  mkdir -p text_to_image_data
  cp ../data/kanji_png_256/* text_to_image_data/
  cp ../data/metadata.jsonl text_to_image_data/
fi

# Ensure metadata.jsonl uses 'file_name' as the key
sed -i 's/"image":/"file_name":/g' text_to_image_data/metadata.jsonl


#Run training
accelerate launch train_text_to_image_lora.py \
  --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
  --train_data_dir="text_to_image_data" \
  --output_dir="kanji_text_to_image_lora" \
  --resolution=256 \
  --train_batch_size=4 \
  --gradient_accumulation_steps=1 \
  --max_train_steps=10000 \
  --learning_rate=1e-4 \
  --checkpointing_steps=1000 \
  --validation_prompt="love; affection; favourite" \
  --num_validation_images=4 \
  --validation_epochs=5 \
  --seed=42 \
  --mixed_precision="fp16" \
  --gradient_checkpointing \
  --enable_xformers_memory_efficient_attention

echo "Text-to-Image LoRA training complete! Check kanji_text_to_image_lora/ for weights."
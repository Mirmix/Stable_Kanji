accelerate launch train_dreambooth_lora.py \
  --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
  --instance_data_dir="train_images" \
  --instance_prompt="a kanji character" \
  --output_dir="kanji_lora_output" \
  --resolution=512 \
  --train_batch_size=4 \
  --gradient_accumulation_steps=1 \
  --learning_rate=1e-4 \
  --max_train_steps=10000 \
  --checkpointing_steps=1000 \
  --seed=42

echo "DreamBooth LoRA training complete! Check kanji_lora_output/ for weights."
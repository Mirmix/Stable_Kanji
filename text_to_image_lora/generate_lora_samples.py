import torch
from diffusers import StableDiffusionPipeline
import os

# --- CONFIGURATION ---
BASE_MODEL = "runwayml/stable-diffusion-v1-5"  # or v1-4, or your base model
LORA_WEIGHTS = "kanji_text_to_image_lora"      # folder with LoRA weights (change for DreamBooth)
OUTPUT_DIR = "lora_samples"
PROMPTS = [
    "love; affection; favourite",
    "YouTube; video sharing; streaming",
    "Elon Musk; Tesla; SpaceX",
    "Gundam; mecha; robot anime",
    "a kanji character for democracy",
    "a kanji character for smartphone"
]
NUM_IMAGES = 4  # per prompt

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- LOAD PIPELINE ---
pipe = StableDiffusionPipeline.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    safety_checker=None,
    requires_safety_checker=False
)
pipe.load_lora_weights(LORA_WEIGHTS)
if torch.cuda.is_available():
    pipe = pipe.to("cuda")

# --- GENERATE SAMPLES ---
for prompt in PROMPTS:
    images = pipe(
        prompt=prompt,
        num_inference_steps=30,
        guidance_scale=7.5,
        num_images_per_prompt=NUM_IMAGES
    ).images
    for i, img in enumerate(images):
        img.save(os.path.join(OUTPUT_DIR, f"{prompt.replace(' ', '_')[:20]}_{i}.png"))
        print(f"Saved: {prompt} [{i}]")

print(f"All samples saved to {OUTPUT_DIR}/")
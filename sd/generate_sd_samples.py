import torch
from diffusers import StableDiffusionPipeline, UNet2DConditionModel
from diffusers.utils import make_image_grid
from transformers import CLIPTokenizer, CLIPFeatureExtractor
import os

# Configuration
CHECKPOINT_PATH = "sd_pretrained_output/checkpoint-20000"
BASE_MODEL = "CompVis/stable-diffusion-v1-4"
OUTPUT_DIR = "sd_scratch_samples"
PROMPTS = [
    "love; affection; favourite",
    "Artificial Intelligence",
]
NUM_IMAGES = 4

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Use float32 for all components to avoid dtype mismatch
base_pipe = StableDiffusionPipeline.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float32,  # Changed to float32
    safety_checker=None,
    requires_safety_checker=False
)

# Load your trained UNet in float32
trained_unet = UNet2DConditionModel.from_pretrained(
    f"{CHECKPOINT_PATH}/unet",
    torch_dtype=torch.float32  # Ensure float32
)

# Create new pipeline with your trained UNet and base components
pipe = StableDiffusionPipeline(
    unet=trained_unet,
    vae=base_pipe.vae,
    text_encoder=base_pipe.text_encoder,
    tokenizer=base_pipe.tokenizer,
    scheduler=base_pipe.scheduler,
    feature_extractor=base_pipe.feature_extractor,
    safety_checker=None,
    requires_safety_checker=False
)

if torch.cuda.is_available():
    pipe = pipe.to("cuda")

# Generate samples
for prompt in PROMPTS:
    print(f"Generating samples for: '{prompt}'")
    
    images = pipe(
        prompt=prompt,
        num_inference_steps=30,
        guidance_scale=7.5,
        num_images_per_prompt=NUM_IMAGES
    ).images
    
    # Save individual images
    for i, image in enumerate(images):
        filename = f"sd_checkpoint_{prompt.replace(' ', '_')[:20]}_{i}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        image.save(filepath)
        print(f"  Saved: {filepath}")
    
    # Create and save grid image (2x2 grid)
    grid = make_image_grid(images, rows=2, cols=2)
    grid_filename = f"sd_grid_{prompt.replace(' ', '_')[:20]}.png"
    grid_filepath = os.path.join(OUTPUT_DIR, grid_filename)
    grid.save(grid_filepath)
    print(f"  Saved grid: {grid_filepath}")

print(f"All samples and grids saved to {OUTPUT_DIR}/")
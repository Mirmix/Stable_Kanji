import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import make_image_grid
import os

# Paths
LORA_PATH = "kanji_dreambooth_lora_output"
BASE_MODEL = "runwayml/stable-diffusion-v1-5"
OUTPUT_DIR = "generated_samples"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_model():
    """Load the base model with LoRA weights"""
    pipe = StableDiffusionPipeline.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        safety_checker=None,
        requires_safety_checker=False
    )
    
    # Load LoRA weights
    pipe.load_lora_weights(LORA_PATH)
    
    # Use DPM++ 2M scheduler for better quality
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    
    # Move to GPU if available
    if torch.cuda.is_available():
        pipe = pipe.to("cuda")
    
    return pipe

def generate_samples(pipe, prompts, num_samples=4):
    """Generate samples for each prompt"""
    for i, prompt in enumerate(prompts):
        print(f"Generating samples for: '{prompt}'")
        
        # Generate multiple samples
        images = pipe(
            prompt=prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            num_images_per_prompt=num_samples
        ).images
        
        # Save individual images
        for j, image in enumerate(images):
            filename = f"sample_{i}_{j}_{prompt.replace(' ', '_')[:20]}.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            image.save(filepath)
            print(f"  Saved: {filepath}")
        
        # Create and save grid
        grid = make_image_grid(images, rows=2, cols=2)
        grid_filename = f"grid_{i}_{prompt.replace(' ', '_')[:20]}.png"
        grid_filepath = os.path.join(OUTPUT_DIR, grid_filename)
        grid.save(grid_filepath)
        print(f"  Saved grid: {grid_filepath}")

def main():
    # Test prompts - mix of traditional concepts and modern ones
    test_prompts = [
        "a kanji character for love",
        "a kanji character for technology",
        "a kanji character for Elon Musk",
        "a kanji character for YouTube",
        "a kanji character for artificial intelligence",
        "a kanji character for Gundam",
        "a kanji character for internet",
        "a kanji character for democracy",
        "a kanji character for coffee",
        "a kanji character for smartphone"
    ]
    
    print("Loading model with LoRA weights...")
    pipe = load_model()
    
    print("Generating samples...")
    generate_samples(pipe, test_prompts, num_samples=4)
    
    print(f"\nSamples saved to: {OUTPUT_DIR}")
    print("Check the generated images to see how well your model learned to create Kanji-like characters!")

if __name__ == "__main__":
    main() 
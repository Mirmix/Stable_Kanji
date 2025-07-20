# Kanji Diffusion: Generating Kanji-like Glyphs from English Prompts


## Environment Setup

```bash
conda create -n kanji-diff python=3.10 -y
conda activate kanji-diff
conda install pip -y
pip install -r requirements.txt
```


## Inspiration & Credits
This project was inspired by these tweets:
- [![hardmaru tweet](https://img.shields.io/badge/Tweet-%40hardmaru-1da1f2?logo=twitter&style=flat)](https://x.com/hardmaru/status/1611237067589095425)
- [![enpitsu tweet](https://img.shields.io/badge/Tweet-%40enpitsu-1da1f2?logo=twitter&style=flat)](https://x.com/enpitsu/status/1610587513059684353)

Project by Nail Ibrahimli as a fun weekend project.

## Introduction
This fun project explores SD-based generative modeling for Japanese Kanji-like characters from English definitions. The goal is to enable a diffusion model to hallucinate plausible Kanji for concepts that do not have traditional characters (e.g., "Artificial Intelligence").

## Data Preprocessing Pipeline
- **Source:** KANJIDIC2 (Kanji + English meanings) and KanjiVG (SVG strokes)
- **Steps:**
  1. Parse KANJIDIC2 to extract Kanji and English meanings
  2. Extract and clean SVGs for each Kanji
  3. Render SVGs to black-on-white PNGs (128x128, 256x256)
  4. Pair each image with its English meanings
  5. Prepare data for training (DreamBooth, LoRA and vanilla text-to-image)

## Training Approaches

### DreamBooth LoRA (10K iters)
- **Prompt:** Uses a single prompt for all images (e.g., "a kanji character")
- **Strengths:** Simple, good for style transfer
- **Limitations:** Cannot map specific English meanings to glyphs; less flexible for novel concepts

### Text-to-Image LoRA (10K iters)
- **Prompt:** Uses per-image prompts
- **Strengths:** Learns to map specific English meanings to glyphs optimizing less parameters; strongly rely on prior  knowledge of network
- **Limitations:** Sligtly more complex task to learn, requires prompt-image mapping, and kanji images are not semantically meaningful

### Text-to-Image SD (20K iters)
- **Prompt:** Uses per-image prompts
- **Strengths:** Learns to map specific English meanings to glyphs optimizing; can overwrite prior knowledge
- **Limitations:** Complex task to learn, requires prompt-image mapping, and kanji images are not semantically meaningful

## Sample Results

Teaser images from the results (see `sample_results/` for more):

### DreamBooth LoRA
- Prompt: "a kanji character for love"
  - ![DreamBooth LoRA Love](sample_results/dreambooth_lora_samples/grid_0_a_kanji_character_fo.png)
- Prompt: "a kanji character for Artificial Intelligence"
  - ![DreamBooth LoRA Artificial Intelligence](sample_results/dreambooth_lora_samples/grid_4_a_kanji_character_fo.png)

### Text-to-Image LoRA
- Prompt: "love; affection; favourite"
  - ![Text-to-Image LoRA Love](sample_results/text_to_image_lora_samples/text2img_grid_0_love\;_affection\;_fav.png )
- Prompt: "Artificial Intelligence"
  - ![Text-to-Image LoRA Artificial Intelligence](sample_results/text_to_image_lora_samples/text2img_grid_4_artificial_intellige.png)

### Stable Diffusion: finetuning unet
- Prompt: "love; affection; favourite"
  - ![SD finetune Love](sample_results/sd_pretrained_samples/sd_grid_love;_affection;_fav.png )
- Prompt: "Artificial Intelligence"
  - ![SD finetune Artificial Intelligence](sample_results/sd_pretrained_samples/sd_grid_Artificial_Intellige.png)

### Stable Diffusion: training unet from scratch
- Prompt: "love; affection; favourite"
  - ![SD train Love](sample_results/sd_scratch_samples/sd_grid_love;_affection;_fav.png )
- Prompt: "Artificial Intelligence"
  - ![SD train Artificial Intelligence](sample_results/sd_scratch_samples/sd_grid_Artificial_Intellige.png)


*See the `sample_results/` folder for more generated examples.*

## Discussion
- **DreamBooth LoRA** is best for learning a style (Kanji-ness) but not for semantic mapping.
- **Text-to-Image LoRA** enables the model to generate plausible Kanji for arbitrary English prompts.

## Reproducibility
- All scripts and data processing steps are provided in `data_processing/`.
- Training and sample generation scripts are in `dreambooth_lora/` and `text_to_image_lora/`.
- Environment setup instructions are included.
- Results can be reproduced by following the README files in each folder.

---

## TODO (potential improvements)
- Implementing and train (VAE+UNet) a small Stable Diffusion model from scratch on the Kanji dataset and compare results.
- Disentangle Kanji words that have multiple meanings (e.g., "love" vs. "affection")
- Try other baselines (e.g. rectified flow models)

*For questions or contributions, contact the maintainer.* 
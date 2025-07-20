# Data Processing Pipeline

This folder contains scripts and instructions to build a dataset of (English, Kanji image) pairs for generative modeling.

## Steps

### 1. Parse KANJIDIC2
Extract Kanji and English meanings:
```bash
python parse_kanjidic2.py
```

### 2. Extract and Clean SVGs
Extract SVGs for each Kanji and clean them:
```bash
python extract_and_clean_kanjivg_svgs.py
```

### 3. Convert SVGs to PNGs
Render SVGs to 128x128 and 256x256 black-on-white PNGs:
```bash
python svg_to_png.py
```

### 4. Create Dataset Mapping
Pair each Kanji image with its English meanings:
```bash
python create_dataset_mapping.py
```

### 5. Prepare Data for LoRA Training
- For DreamBooth LoRA:
  ```bash
  python prepare_lora_data.py
  ```
- For Text-to-Image LoRA:
  ```bash
  python prepare_text_to_image_data.py
  ```

## Outputs
- Cleaned SVGs: `kanji_svgs_clean/`
- PNGs: `kanji_png_128/`, `kanji_png_256/`
- Dataset mapping: `kanji_image_mapping.csv`, `kanji_image_mapping.json`
- LoRA-ready data: `train_images/`, `train_prompts.txt`, `text_to_image_data/`, `metadata.jsonl`

## Notes
- All scripts are reproducible and can be run in sequence.
- See each script for additional options or details. 
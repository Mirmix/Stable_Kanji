import os
import shutil
import pandas as pd

MAPPING_CSV = 'kanji_image_mapping.csv'
SRC_IMG_DIR = 'kanji_png_256'
DST_IMG_DIR = 'train_images'
PROMPT_FILE = 'train_prompts.txt'

os.makedirs(DST_IMG_DIR, exist_ok=True)

def main():
    df = pd.read_csv(MAPPING_CSV)
    prompts = []
    for _, row in df.iterrows():
        kanji = row['kanji']
        meanings = row['meanings']
        hex_code = format(ord(kanji), '05x')
        src_img = os.path.join(SRC_IMG_DIR, f'{hex_code}.png')
        dst_img = os.path.join(DST_IMG_DIR, f'{hex_code}.png')
        if os.path.exists(src_img):
            shutil.copy2(src_img, dst_img)
            prompts.append(meanings)
    with open(PROMPT_FILE, 'w', encoding='utf-8') as f:
        for prompt in prompts:
            f.write(str(prompt) + '\n')
    print(f"Copied {len(prompts)} images to {DST_IMG_DIR} and wrote prompts to {PROMPT_FILE}")

if __name__ == '__main__':
    main() 
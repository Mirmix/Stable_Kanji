import os
import pandas as pd
import json

KANJI_CSV = 'kanji_meanings.csv'
PNG_DIR_128 = 'kanji_png_128'
PNG_DIR_256 = 'kanji_png_256'
CSV_OUT = 'kanji_image_mapping.csv'
JSON_OUT = 'kanji_image_mapping.json'

def main():
    df = pd.read_csv(KANJI_CSV)
    records = []
    for _, row in df.iterrows():
        kanji = row['kanji']
        meanings = row['meanings']
        hex_code = format(ord(kanji), '05x')
        png_128 = os.path.join(PNG_DIR_128, f'{hex_code}.png')
        png_256 = os.path.join(PNG_DIR_256, f'{hex_code}.png')
        if os.path.exists(png_128) and os.path.exists(png_256):
            records.append({
                'kanji': kanji,
                'meanings': meanings,
                'png_128': png_128,
                'png_256': png_256
            })
    # Save CSV
    pd.DataFrame(records).to_csv(CSV_OUT, index=False)
    # Save JSON
    with open(JSON_OUT, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(records)} entries to {CSV_OUT} and {JSON_OUT}")

if __name__ == '__main__':
    main() 
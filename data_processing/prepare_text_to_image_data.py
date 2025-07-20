import os
import shutil
import pandas as pd
import json

MAPPING_CSV = 'kanji_image_mapping.csv'
SRC_IMG_DIR = 'kanji_png_256'
DST_IMG_DIR = 'text_to_image_data'
METADATA_JSONL = os.path.join(DST_IMG_DIR, 'metadata.jsonl')

os.makedirs(DST_IMG_DIR, exist_ok=True)

def main():
    df = pd.read_csv(MAPPING_CSV)
    metadata_records = []
    
    for _, row in df.iterrows():
        kanji = row['kanji']
        meanings = row['meanings']
        hex_code = format(ord(kanji), '05x')
        
        src_img = os.path.join(SRC_IMG_DIR, f'{hex_code}.png')
        dst_img = os.path.join(DST_IMG_DIR, f'{hex_code}.png')
        
        if os.path.exists(src_img):
            # Copy image
            shutil.copy2(src_img, dst_img)
            
            # Add to metadata (JSONL format with correct column names)
            metadata_records.append({
                'file_name': f'{hex_code}.png',  # Changed to 'file_name' as expected by the script
                'text': meanings  # English meanings as the prompt
            })
    
    # Save metadata as JSONL inside the data folder
    with open(METADATA_JSONL, 'w', encoding='utf-8') as f:
        for record in metadata_records:
            f.write(json.dumps(record) + '\n')
    
    # Also save as CSV for reference (in current directory)
    metadata_df = pd.DataFrame(metadata_records)
    metadata_df.to_csv('metadata.csv', index=False)
    
    print(f"Prepared {len(metadata_records)} images for text-to-image training")
    print(f"Images copied to: {DST_IMG_DIR}")
    print(f"Metadata saved to: {METADATA_JSONL} (JSONL format)")
    print(f"Sample metadata entries:")
    print(metadata_records[:3])

if __name__ == '__main__':
    main() 
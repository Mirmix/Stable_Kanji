import lxml.etree as ET
import os
import pandas as pd

KANJIVG_PATH = 'data_xml/kanjivg-20220427.xml'
KANJI_CSV = 'kanji_meanings.csv'
OUTPUT_DIR = 'kanji_svgs'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def unicode_hex(kanji):
    return format(ord(kanji), '05x')

def main():
    # Load Kanji list
    df = pd.read_csv(KANJI_CSV)
    kanji_set = set(df['kanji'])

    # Parse KanjiVG XML
    context = ET.iterparse(KANJIVG_PATH, events=('end',), tag='kanji')
    count = 0
    for event, elem in context:
        kanji_id = elem.get('id')
        if not kanji_id or not kanji_id.startswith('kvg:kanji_'):
            elem.clear()
            continue
        # KanjiVG uses Unicode hex in id, e.g. kvg:kanji_4e00
        hex_code = kanji_id.split('_')[-1]
        kanji_char = chr(int(hex_code, 16))
        if kanji_char not in kanji_set:
            elem.clear()
            continue
        # Wrap the <kanji> element in an <svg> root for standalone SVG
        svg_elem = ET.Element('svg', xmlns="http://www.w3.org/2000/svg",
                              width="109", height="109", viewBox="0 0 109 109")
        for child in elem:
            svg_elem.append(child)
        svg_str = ET.tostring(svg_elem, encoding='utf-8', xml_declaration=True)
        out_path = os.path.join(OUTPUT_DIR, f'{hex_code}.svg')
        with open(out_path, 'wb') as f:
            f.write(svg_str)
        count += 1
        elem.clear()
    print(f"Extracted {count} SVGs to {OUTPUT_DIR}/ with proper SVG attributes.")

if __name__ == '__main__':
    main() 
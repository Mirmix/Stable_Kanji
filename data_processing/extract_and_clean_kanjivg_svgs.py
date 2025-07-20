import lxml.etree as ET
import os
import pandas as pd
import re

KANJIVG_PATH = 'data_xml/kanjivg-20220427.xml'
KANJI_CSV = 'kanji_meanings.csv'
OUTPUT_DIR = 'kanji_svgs_clean'

os.makedirs(OUTPUT_DIR, exist_ok=True)

SVG_WIDTH = '109'
SVG_HEIGHT = '109'
SVG_VIEWBOX = '0 0 109 109'

# Remove kvg: namespace from tag and attribute
KVG_NS = '{http://kanjivg.tagaini.net}'
def strip_kvg_ns(tag):
    if tag.startswith(KVG_NS):
        return tag[len(KVG_NS):]
    return tag

def clean_svg_elem(elem):
    elem.tag = strip_kvg_ns(elem.tag)
    # Remove kvg: attributes
    for attr in list(elem.attrib):
        if attr.startswith('{' + 'http://kanjivg.tagaini.net' + '}'):
            del elem.attrib[attr]
    # For <path> elements, set stroke and fill
    if elem.tag == 'path':
        elem.set('stroke', 'black')
        elem.set('fill', 'none')
    for child in elem:
        clean_svg_elem(child)

def main():
    df = pd.read_csv(KANJI_CSV)
    kanji_set = set(df['kanji'])
    context = ET.iterparse(KANJIVG_PATH, events=('end',), tag='kanji')
    count = 0
    for event, elem in context:
        kanji_id = elem.get('id')
        if not kanji_id or not kanji_id.startswith('kvg:kanji_'):
            elem.clear()
            continue
        hex_code = kanji_id.split('_')[-1]
        kanji_char = chr(int(hex_code, 16))
        if kanji_char not in kanji_set:
            elem.clear()
            continue
        # Clean up namespaces and attributes
        clean_svg_elem(elem)
        svg_elem = ET.Element('svg', xmlns="http://www.w3.org/2000/svg",
                              width=SVG_WIDTH, height=SVG_HEIGHT, viewBox=SVG_VIEWBOX)
        for child in elem:
            svg_elem.append(child)
        svg_str = ET.tostring(svg_elem, encoding='utf-8', xml_declaration=True)
        out_path = os.path.join(OUTPUT_DIR, f'{hex_code}.svg')
        with open(out_path, 'wb') as f:
            f.write(svg_str)
        count += 1
        elem.clear()
    print(f"Extracted and cleaned {count} SVGs to {OUTPUT_DIR}/")

if __name__ == '__main__':
    main() 
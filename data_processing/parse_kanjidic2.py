import lxml.etree as ET
import pandas as pd

KANJIDIC2_PATH = 'data_xml/kanjidic2.xml'
OUTPUT_CSV = 'kanji_meanings.csv'

def parse_kanjidic2(xml_path):
    context = ET.iterparse(xml_path, events=('end',), tag='character')
    kanji_data = []
    for event, elem in context:
        literal = elem.find('literal')
        if literal is None:
            continue
        kanji = literal.text
        meanings = []
        # Find all English meanings (meaning elements with no m_lang attribute)
        for meaning in elem.findall('.//meaning'):
            if meaning.get('m_lang') is None:
                meanings.append(meaning.text)
        if meanings:
            kanji_data.append({'kanji': kanji, 'meanings': ';'.join(meanings)})
        elem.clear()
    return kanji_data

def main():
    kanji_data = parse_kanjidic2(KANJIDIC2_PATH)
    df = pd.DataFrame(kanji_data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {len(df)} kanji to {OUTPUT_CSV}")

if __name__ == '__main__':
    main() 
import os
import cairosvg

SVG_DIR = 'kanji_svgs_clean'
PNG_DIR_128 = 'kanji_png_128'
PNG_DIR_256 = 'kanji_png_256'

os.makedirs(PNG_DIR_128, exist_ok=True)
os.makedirs(PNG_DIR_256, exist_ok=True)

def convert_svg_to_png(svg_path, png_path, size):
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=size, output_height=size, background_color='white')

def main():
    svg_files = [f for f in os.listdir(SVG_DIR) if f.endswith('.svg')]
    for svg_file in svg_files:
        svg_path = os.path.join(SVG_DIR, svg_file)
        png_path_128 = os.path.join(PNG_DIR_128, svg_file.replace('.svg', '.png'))
        png_path_256 = os.path.join(PNG_DIR_256, svg_file.replace('.svg', '.png'))
        convert_svg_to_png(svg_path, png_path_128, 128)
        convert_svg_to_png(svg_path, png_path_256, 256)
    print(f"Converted {len(svg_files)} SVGs to PNGs in {PNG_DIR_128}/ and {PNG_DIR_256}/")

if __name__ == '__main__':
    main() 
import os
from PIL import Image

for folder in ['jewellery-design-html/solystra_assets/collections', 'jewellery-design-html/solystra_assets/categories/zavya_style']:
    if not os.path.exists(folder):
        continue
    print(f"=== {folder} ===")
    for f in sorted(os.listdir(folder)):
        if f.endswith('.webp') or f.endswith('.jpg'):
            p = os.path.join(folder, f)
            try:
                img = Image.open(p).convert('RGB')
                pixel = img.resize((1, 1)).getpixel((0, 0))
                r, g, b = pixel
                is_green = g > (r + 10) and g > (b + 10)
                status = "GREEN DOMINANT" if is_green else "neutral/warm"
                print(f"  {f}: avg RGB=({r:3d}, {g:3d}, {b:3d}) -> {status}")
            except Exception as e:
                print(f"  {f}: error {e}")


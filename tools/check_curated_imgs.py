from PIL import Image

imgs = [
    'jewellery-design-html/solystra_assets/curated/curated_look_second_combo.webp',
    'jewellery-design-html/solystra_assets/curated/curated_look_golden_meadow.webp'
]

for p in imgs:
    im = Image.open(p)
    print(f"{p}: size={im.size}, aspect={im.width/im.height:.3f}")

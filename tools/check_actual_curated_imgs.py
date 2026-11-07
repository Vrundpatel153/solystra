from PIL import Image

for p in [
    'jewellery-design-html/solystra_assets/curated/curated_look_combo2.webp',
    'jewellery-design-html/solystra_assets/curated/curated_look_golden_meadow.webp'
]:
    im = Image.open(p)
    print(f"{p}: size={im.size}, aspect={im.width/im.height:.3f}")

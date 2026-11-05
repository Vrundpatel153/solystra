import os
from PIL import Image

for name in ['cat_bracelets.webp', 'cat_rings.webp', 'cat_earrings.webp', 'cat_anklets.webp']:
    p = os.path.join('jewellery-design-html/solystra_assets/categories', name)
    img = Image.open(p).convert('RGB')
    corner = img.getpixel((10, 10))
    center = img.getpixel((img.width // 2, img.height // 2))
    print(f"{name}: corner RGB={corner}, center RGB={center}")


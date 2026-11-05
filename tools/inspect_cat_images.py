import os
from PIL import Image

for name in ['cat_bracelets.webp', 'cat_rings.webp', 'cat_earrings.webp', 'cat_anklets.webp', 'cat_necklaces.webp', 'cat_complete_sets.webp']:
    p = os.path.join('jewellery-design-html/solystra_assets/categories', name)
    if os.path.exists(p):
        img = Image.open(p)
        print(f"{name}: size={img.size}, mode={img.mode}")


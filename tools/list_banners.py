import os
from PIL import Image

banner_dir = 'jewellery-design-html/solystra_assets/banners'
for f in os.listdir(banner_dir):
    p = os.path.join(banner_dir, f)
    if os.path.isfile(p):
        size = os.path.getsize(p)
        try:
            im = Image.open(p)
            print(f"{f}: {im.size}, {size/1024:.1f} KB")
        except Exception:
            print(f"{f}: {size/1024:.1f} KB (not image)")


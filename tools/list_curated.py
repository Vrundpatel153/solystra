import os
from PIL import Image

curated_dir = 'jewellery-design-html/solystra_assets/drive_curated'
for f in sorted(os.listdir(curated_dir)):
    p = os.path.join(curated_dir, f)
    if os.path.isfile(p):
        size = os.path.getsize(p)
        try:
            im = Image.open(p)
            print(f"{f}: {im.size}, {size/1024:.1f} KB")
        except Exception:
            print(f"{f}: {size/1024:.1f} KB")


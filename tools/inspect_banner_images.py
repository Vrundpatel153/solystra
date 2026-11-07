import os
from PIL import Image

banner_files = [
    'banner-1-pc.png',
    'banner-1-mobile.png',
    'banner-2-pc.png',
    'banner2-mobile.png',
    'Serene Floral Jewelry Portrait.png',
    'Serene Profile with Floral Jewelry.png'
]

for bf in banner_files:
    p = os.path.join('scratch/drive_raw_downloads', bf)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{bf}: size={im.size}, mode={im.mode}")

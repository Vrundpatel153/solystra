from PIL import Image
import os

files = [
    'scratch/drive_downloads_new/banner-3-pc.png',
    'scratch/drive_downloads_new/banner-3-mobile.png',
    'scratch/drive_downloads_new/banner-4-pc.png',
    'scratch/drive_downloads_new/banner-4-mobile.png'
]

for f in files:
    if os.path.exists(f):
        im = Image.open(f)
        print(f"{f}: size={im.size}, mode={im.mode}")
    else:
        print(f"Not found: {f}")

import os
from PIL import Image

photos = {
    'necklaces.webp': ('scratch/drive_photos/DSC02659.JPG', 'portrait'),
    'mangalsutras.webp': ('scratch/drive_photos/DSC02667.JPG', 'landscape'),
    'complete_sets.webp': ('scratch/drive_photos/DSC02668.JPG', 'landscape'),
    'collection_drops.webp': ('scratch/drive_photos/DSC02673.JPG', 'landscape'),
    'collection_ombre.webp': ('scratch/drive_photos/DSC02674.JPG', 'landscape'),
    'chains.webp': ('scratch/drive_photos/DSC02660.JPG', 'landscape'),
}

for target, (src, orientation) in photos.items():
    with Image.open(src) as img:
        w, h = img.size
        print(f"Target: {target} <- {src} ({w}x{h}, {orientation})")


import os
from PIL import Image

thumb_dir = 'scratch/drive_thumbnails'
test_files = ['DSC02730.JPG', 'DSC02738.JPG', 'DSC02739.JPG', 'DSC02845.JPG', 'DSC02850.JPG', 'DSC02915.JPG', 'DSC02925.JPG', 'DSC02930.JPG']

for f in test_files:
    p = os.path.join(thumb_dir, f)
    if os.path.exists(p):
        with Image.open(p) as im:
            print(f"{f}: size={im.size}")

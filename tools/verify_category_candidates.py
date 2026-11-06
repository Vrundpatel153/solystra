import os
from PIL import Image

candidates = {
    'Bracelets & Kadas': ['DSC03085.JPG', 'DSC03086.JPG', 'DSC03087.JPG', 'DSC03088.JPG', 'DSC03089.JPG', 'DSC02915.JPG', 'DSC02920.JPG'],
    'Rings & Bands': ['DSC03011.JPG', 'DSC03012.JPG', 'DSC03013.JPG', 'DSC03014.JPG', 'DSC03050.JPG', 'DSC03052.JPG', 'DSC03115.JPG', 'DSC03116.JPG'],
    'Earrings & Studs': ['DSC03000.JPG', 'DSC03001.JPG', 'DSC03002.JPG', 'DSC03075.JPG', 'DSC03109.JPG', 'DSC03110.JPG', 'DSC03117.JPG'],
    'Necklaces & Pendants': ['DSC03100.JPG', 'DSC03101.JPG', 'DSC03040.JPG', 'DSC02720.JPG', 'DSC02721.JPG', 'DSC02722.JPG', 'DSC02810.JPG'],
    'Complete Suites & Sets': ['DSC03045.JPG', 'DSC03060.JPG', 'DSC03070.JPG', 'DSC03090.JPG', 'DSC03095.JPG', 'DSC03105.JPG']
}

thumb_dir = 'scratch/drive_thumbnails'

for cat, files in candidates.items():
    print(f"\n=== {cat} ===")
    for f in files:
        p = os.path.join(thumb_dir, f)
        if os.path.exists(p):
            with Image.open(p) as im:
                print(f"  {f}: size={im.size}")

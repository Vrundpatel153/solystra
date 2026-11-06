import os
from PIL import Image
import numpy as np

src_dir = 'scratch/curated_highres'
models = [
    'hero_1_heart_yellow_DSC02721.jpg',
    'hero_2_pearl_blazer_DSC02810.jpg',
    'hero_3_tennis_green_DSC02915.jpg',
    'hero_4_tiara_blazer_DSC02831.jpg'
]

for m in models:
    p = os.path.join(src_dir, m)
    with Image.open(p) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        arr = np.array(rgb)
        left_strip = arr[:, :50].mean(axis=(0, 1)).astype(int).tolist()
        right_strip = arr[:, -50:].mean(axis=(0, 1)).astype(int).tolist()
        top_strip = arr[:50, :].mean(axis=(0, 1)).astype(int).tolist()
        print(f"{m}: size=({w}x{h}), left={left_strip}, right={right_strip}, top={top_strip}")


import os
from PIL import Image
import numpy as np

src_dir = 'jewellery-design-html/model_candidates_thumbs'
files = sorted(os.listdir(src_dir))

print(f"Inspecting {len(files)} candidate images...")

for f in files:
    p = os.path.join(src_dir, f)
    with Image.open(p) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        arr = np.array(rgb)
        
        # Check colors of clothing (bottom 30%)
        bot = arr[int(h*0.7):, :]
        bot_mean = np.mean(bot, axis=(0,1)).astype(int).tolist()
        
        # Check colors of middle (neck/face)
        mid = arr[int(h*0.25):int(h*0.65), :]
        mid_mean = np.mean(mid, axis=(0,1)).astype(int).tolist()
        
        # Check top (hair/head)
        top = arr[:int(h*0.25), :]
        top_mean = np.mean(top, axis=(0,1)).astype(int).tolist()
        
        print(f"{f}: size=({w}x{h}), top={top_mean}, mid={mid_mean}, bot={bot_mean}")


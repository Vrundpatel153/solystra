import os
import json
from PIL import Image
import numpy as np

thumb_dir = 'scratch/drive_thumbnails'
files = sorted([f for f in os.listdir(thumb_dir) if f.upper().endswith('.JPG')])

print(f"Auditing all {len(files)} Drive images...")

catalog = []

for idx, f in enumerate(files):
    p = os.path.join(thumb_dir, f)
    try:
        im = Image.open(p)
        w, h = im.size
        ratio = w / float(h)
        orientation = "landscape" if ratio > 1.15 else ("portrait" if ratio < 0.88 else "square")
        
        arr = np.array(im.convert('RGB'))
        mean_rgb = np.mean(arr, axis=(0, 1)).astype(int).tolist()
        
        # Series detection
        seq_num = int(f.replace('DSC', '').replace('.JPG', ''))
        
        # Series grouping
        if 2719 <= seq_num <= 2799:
            series = "Yellow Top / Solitaire Heart & Layering"
        elif 2800 <= seq_num <= 2899:
            series = "Black Blazer / Pearls & Tiara Solitaire"
        elif 2900 <= seq_num <= 2999:
            series = "Sage Green Dress / Austrian Tennis Bracelet & Rings"
        elif 3000 <= seq_num <= 3099:
            series = "Emerald Velvet & Still Life Macro Jewelry Details"
        else:
            series = "Lookbook & Signature Suites"
            
        catalog.append({
            'filename': f,
            'seq': seq_num,
            'series': series,
            'w': w,
            'h': h,
            'ratio': round(ratio, 2),
            'orientation': orientation,
            'mean_rgb': mean_rgb
        })
    except Exception as e:
        print(f"Error reading {f}: {e}")

with open('scratch/catalog_398_audit.json', 'w', encoding='utf-8') as f_out:
    json.dump(catalog, f_out, indent=2)

print(f"Saved catalog_398_audit.json with {len(catalog)} analyzed photos.")

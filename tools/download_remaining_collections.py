import os
import json
import urllib.request
from PIL import Image

with open('scratch/all_drive_jpgs.json', 'r') as f:
    drive_data = json.load(f)

remaining = {
    "collection_drops": {"file": "DSC02862.JPG", "box": (0.15, 0.05, 0.85, 0.95)},
    "collection_dainty": {"file": "DSC02741.JPG", "box": (0.1, 0.1, 0.9, 0.9)},
    "collection_ombre": {"file": "DSC02726.JPG", "box": (0.15, 0.05, 0.85, 0.95)},
    "collection_tennis": {"file": "DSC02950.JPG", "box": (0.15, 0.1, 0.85, 0.9)}
}

out_dir = 'jewellery-design-html/solystra_assets/drive_curated'
headers = {'User-Agent': 'Mozilla/5.0'}

for key, meta in remaining.items():
    fn = meta['file']
    fid = drive_data.get(fn)
    dest_path = os.path.join(out_dir, f"{key}.webp")
    if os.path.exists(dest_path):
        print(f"Already exists: {key}")
        continue
    
    print(f"Fetching {key} ({fn}, fid={fid})...")
    if fid:
        url = f"https://lh3.googleusercontent.com/u/0/d/{fid}=w1200"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                temp_raw = f"scratch/temp_{fn}"
                with open(temp_raw, 'wb') as tf:
                    tf.write(data)
                
                with Image.open(temp_raw) as img:
                    w, h = img.size
                    bx1, by1, bx2, by2 = meta['box']
                    crop_box = (int(bx1 * w), int(by1 * h), int(bx2 * w), int(by2 * h))
                    cropped = img.crop(crop_box)
                    cropped = cropped.convert('RGB')
                    cropped.save(dest_path, 'WEBP', quality=90)
                    print(f"  Saved {dest_path} ({cropped.size})")
        except Exception as e:
            print(f"  Error on {key}: {e}")
            # Fallback to drive_thumbs
            thumb_path = f"jewellery-design-html/drive_thumbs/{fn}"
            if os.path.exists(thumb_path):
                with Image.open(thumb_path) as img:
                    w, h = img.size
                    bx1, by1, bx2, by2 = meta['box']
                    crop_box = (int(bx1 * w), int(by1 * h), int(bx2 * w), int(by2 * h))
                    cropped = img.crop(crop_box)
                    cropped = cropped.convert('RGB')
                    cropped.save(dest_path, 'WEBP', quality=90)
                    print(f"  Fallback saved from thumb: {dest_path}")

import os
import json
import urllib.request
from PIL import Image

with open('scratch/all_drive_jpgs.json', 'r') as f:
    drive_data = json.load(f)

# The Curated Selection from Drive
curation = {
    # 6 Categories (1:1 Square)
    "categories": {
        "necklaces": {"file": "DSC02735.JPG", "label": "Necklaces & Pendants", "box": (0.15, 0.1, 0.85, 0.8)},
        "earrings": {"file": "DSC02859.JPG", "label": "Earrings & Studs", "box": (0.05, 0.25, 0.75, 0.95)},
        "bracelets": {"file": "DSC02820.JPG", "label": "Bracelets & Kadas", "box": (0.2, 0.25, 0.8, 0.85)},
        "rings": {"file": "DSC03110.JPG", "label": "Rings & Bands", "box": (0.2, 0.2, 0.8, 0.8)},
        "anklets": {"file": "DSC02738.JPG", "label": "Anklets & Payals", "box": (0.25, 0.1, 0.85, 0.7)},
        "complete_sets": {"file": "DSC02923.JPG", "label": "Gift Sets & Suites", "box": (0.1, 0.15, 0.9, 0.95)}
    },
    # 5 Curated Collections (303:423 Portrait)
    "collections": {
        "collection_links": {"file": "DSC02753.JPG", "label": "Links & Layers", "box": (0.1, 0.05, 0.9, 0.95)},
        "collection_drops": {"file": "DSC02862.JPG", "label": "Drops & Halo", "box": (0.15, 0.05, 0.85, 0.95)},
        "collection_dainty": {"file": "DSC02741.JPG", "label": "Dainty Steps", "box": (0.1, 0.1, 0.9, 0.9)},
        "collection_ombre": {"file": "DSC02726.JPG", "label": "Daily Luxe", "box": (0.15, 0.05, 0.85, 0.95)},
        "collection_tennis": {"file": "DSC02950.JPG", "label": "Tennis Fever", "box": (0.15, 0.1, 0.85, 0.9)}
    }
}

out_dir = 'jewellery-design-html/solystra_assets/drive_curated'
os.makedirs(out_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

# Download high-res from Drive and crop
all_items = {}
all_items.update(curation['categories'])
all_items.update(curation['collections'])

for key, meta in all_items.items():
    fn = meta['file']
    fid = drive_data.get(fn)
    dest_path = os.path.join(out_dir, f"{key}.webp")
    
    print(f"Processing {key} ({fn})...")
    if fid:
        url = f"https://lh3.googleusercontent.com/u/0/d/{fid}=w1200"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                temp_raw = f"scratch/temp_{fn}"
                with open(temp_raw, 'wb') as tf:
                    tf.write(data)
                
                # Open with PIL
                with Image.open(temp_raw) as img:
                    w, h = img.size
                    bx1, by1, bx2, by2 = meta['box']
                    crop_box = (int(bx1 * w), int(by1 * h), int(bx2 * w), int(by2 * h))
                    cropped = img.crop(crop_box)
                    
                    # Convert to RGB and save webp
                    cropped = cropped.convert('RGB')
                    cropped.save(dest_path, 'WEBP', quality=90)
                    print(f"  -> Saved {dest_path} ({cropped.size})")
        except Exception as e:
            print(f"  -> Error: {e}")

print("\nAll Drive curated assets downloaded and prepared!")

import os
import urllib.request
from PIL import Image

RAW_DIR = os.path.abspath("scratch/curated_raw")
WEBP_DIR = os.path.abspath("jewellery-design-html/solystra_assets/curated")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(WEBP_DIR, exist_ok=True)

files = [
    {
        "id": "10W0kgqgRUgsdtGi-VXVjRM-W9hz5j9Lz",
        "name": "second_combo.png",
        "webp": "curated_look_combo2.webp"
    },
    {
        "id": "1EQeLGhm4iK3sMYILjHju5mSxRhBlZ5nF",
        "name": "golden_meadow_set_combo.png",
        "webp": "curated_look_golden_meadow.webp"
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for item in files:
    raw_path = os.path.join(RAW_DIR, item['name'])
    webp_path = os.path.join(WEBP_DIR, item['webp'])
    
    # Try downloading via direct drive url
    url = f"https://drive.usercontent.google.com/download?id={item['id']}&export=download&authuser=0"
    print(f"Downloading {item['name']} from {url}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp, open(raw_path, 'wb') as out:
            out.write(resp.read())
        size = os.path.getsize(raw_path)
        print(f"Downloaded {item['name']}: {size} bytes")
        
        # Convert to high-quality WebP
        with Image.open(raw_path) as img:
            print(f"Image dimensions: {img.size}, mode: {img.mode}")
            # Ensure RGB
            if img.mode in ('RGBA', 'LA'):
                # Check if alpha is needed or transparent
                img.save(webp_path, 'WEBP', quality=92, method=6)
            else:
                img.convert('RGB').save(webp_path, 'WEBP', quality=92, method=6)
        
        print(f"Converted to {item['webp']}: {os.path.getsize(webp_path)} bytes")
        
    except Exception as e:
        print(f"Error downloading {item['name']}: {e}")


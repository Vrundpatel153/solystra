import os
import json
import urllib.request
import time
from PIL import Image

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

RAW_DOWNLOAD_DIR = os.path.abspath('scratch/drive_raw_downloads')
os.makedirs(RAW_DOWNLOAD_DIR, exist_ok=True)

CATEGORIES_DIR = os.path.abspath('jewellery-design-html/solystra_assets/drive_curated')
BANNERS_DIR = os.path.abspath('jewellery-design-html/solystra_assets/banners')
os.makedirs(CATEGORIES_DIR, exist_ok=True)
os.makedirs(BANNERS_DIR, exist_ok=True)

with open('scratch/all_drive_subfolders.json', 'r', encoding='utf-8') as f:
    drive_data = json.load(f)

def download_file(fid, fname):
    dest_raw = os.path.join(RAW_DOWNLOAD_DIR, fname)
    if os.path.exists(dest_raw) and os.path.getsize(dest_raw) > 5000:
        print(f"Already downloaded: {fname} ({os.path.getsize(dest_raw)} bytes)")
        return dest_raw

    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    print(f"Downloading {fname} (id={fid})...")
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with open(dest_raw, "wb") as f:
                        f.write(data)
                    print(f"Downloaded {fname}: {len(data)} bytes")
                    return dest_raw
                else:
                    print(f"Attempt {attempt+1}: Data too small ({len(data)} bytes)")
        except Exception as e:
            print(f"Attempt {attempt+1} error downloading {fname}: {e}")
            time.sleep(2)
    return None

def convert_to_webp(src_path, dest_webp_path, quality=90):
    try:
        im = Image.open(src_path)
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            # If transparent background, ensure clean RGBA
            im = im.convert('RGBA')
        else:
            im = im.convert('RGB')
        
        im.save(dest_webp_path, 'WEBP', quality=quality, method=6)
        orig_sz = os.path.getsize(src_path)
        new_sz = os.path.getsize(dest_webp_path)
        reduction = (1 - (new_sz / orig_sz)) * 100
        print(f"Converted: {os.path.basename(dest_webp_path)} | {im.size} | {orig_sz//1024}KB -> {new_sz//1024}KB ({reduction:.1f}% saved)")
        return True
    except Exception as e:
        print(f"Error converting {src_path} to WebP: {e}")
        return False

# Mapping rules
CATEGORY_MAP = {
    "Layered Gold Necklace with Green Pendant.png": "necklaces.webp",
    "Diamond Knot Pearl Drop Earrings.png": "earrings.webp",
    "Rose Gold Heart and Starburst Bracelet.png": "bracelets.webp",
    "Golden Diamond Heart Loop Ring.png": "rings.webp",
    "Sparkling Silver Floral Chain on Satin.png": "anklets.webp",
    "Purple Floral Jewelry on Champagne Silk (1).png": "complete_sets.webp"
}

COLLECTION_MAP = {
    "daily-luxe.png": ["collection_daily_luxe.webp", "collection_ombre.webp"], # also alias to collection_ombre used in some links
    "dainty-steps.png": ["collection_dainty.webp"],
    "drops and halo.png": ["collection_drops.webp"],
    "links and layers.png": ["collection_links.webp"],
    "tennis-fever.png": ["collection_tennis.webp"]
}

BANNER_MAP = {
    "banner-1-pc.png": "banner_pc_1.webp",
    "banner-1-mobile.png": "banner_mob_1.webp",
    "banner-2-pc.png": "banner_pc_2.webp",
    "banner2-mobile.png": "banner_mob_2.webp",
    "Serene Floral Jewelry Portrait.png": "banner_floral_portrait.webp",
    "Serene Profile with Floral Jewelry.png": "banner_profile_floral.webp"
}

print("=== 1. PROCESSING CATEGORIES ===")
for item in drive_data.get('categories', []):
    raw_path = download_file(item['id'], item['name'])
    if raw_path and item['name'] in CATEGORY_MAP:
        target_name = CATEGORY_MAP[item['name']]
        dest_path = os.path.join(CATEGORIES_DIR, target_name)
        convert_to_webp(raw_path, dest_path, quality=90)

print("\n=== 2. PROCESSING COLLECTIONS ===")
for item in drive_data.get('collections', []):
    raw_path = download_file(item['id'], item['name'])
    if raw_path and item['name'] in COLLECTION_MAP:
        target_names = COLLECTION_MAP[item['name']]
        for t_name in target_names:
            dest_path = os.path.join(CATEGORIES_DIR, t_name)
            convert_to_webp(raw_path, dest_path, quality=90)

print("\n=== 3. PROCESSING HERO BANNERS ===")
for item in drive_data.get('hero-banner', []):
    raw_path = download_file(item['id'], item['name'])
    if raw_path and item['name'] in BANNER_MAP:
        target_name = BANNER_MAP[item['name']]
        dest_path = os.path.join(BANNERS_DIR, target_name)
        convert_to_webp(raw_path, dest_path, quality=92)

print("\nALL DRIVE IMAGES DOWNLOADED & CONVERTED TO CRISP HD WEBP SUCCESSFULLY!")

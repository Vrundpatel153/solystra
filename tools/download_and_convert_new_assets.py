import os
import urllib.request
import time
from PIL import Image

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

DOWNLOAD_DIR = os.path.abspath('scratch/drive_downloads_new')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

TARGET_ASSETS = {
    # Collections
    "daily_luxe": {
        "id": "11fdmWM7RDjPAAM7sDkWQpgmfM1Hq9I2Z",
        "raw": os.path.join(DOWNLOAD_DIR, "daily_luxe.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/drive_curated/collection_daily_luxe.webp")
    },
    "dainty_steps": {
        "id": "1zVGnF45A_uDitVV_5mKyWg0c8J46JCkR",
        "raw": os.path.join(DOWNLOAD_DIR, "dainty_steps.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/drive_curated/collection_dainty.webp")
    },
    "drops_halo": {
        "id": "1-sfL3MJmTql8ZOuYIwlC2hNDt00tR975",
        "raw": os.path.join(DOWNLOAD_DIR, "drops_halo.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/drive_curated/collection_drops.webp")
    },
    "links_layers": {
        "id": "115SoqiHF1S4QboADxYRGOUWVT9pF1Nb2",
        "raw": os.path.join(DOWNLOAD_DIR, "links_layers.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/drive_curated/collection_links.webp")
    },
    "tennis_fever": {
        "id": "1skxM8MQcIegaz_RS3vUSLUfv8L4_0CTm",
        "raw": os.path.join(DOWNLOAD_DIR, "tennis_fever.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/drive_curated/collection_tennis.webp")
    },
    # Banners
    "banner_3_pc": {
        "id": "14Hep9zRcnhDa5kP4NbGq1k7FAf9rHoR5",
        "raw": os.path.join(DOWNLOAD_DIR, "banner_3_pc.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/banners/banner_pc_3.webp")
    },
    "banner_3_mob": {
        "id": "158B9MS_C8BzEcDfLYN8KFWRbI2w1eCxf",
        "raw": os.path.join(DOWNLOAD_DIR, "banner_3_mob.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/banners/banner_mob_3.webp")
    },
    "banner_4_pc": {
        "id": "1NdhAE8Xny4PCzTeJwG9EktsIA5vYKXo1",
        "raw": os.path.join(DOWNLOAD_DIR, "banner_4_pc.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/banners/banner_pc_4.webp")
    },
    "banner_4_mob": {
        "id": "1mElUMqtmgWJTBmy5Ma8vDq0mcOi3XlkQ",
        "raw": os.path.join(DOWNLOAD_DIR, "banner_4_mob.png"),
        "dest": os.path.abspath("jewellery-design-html/solystra_assets/banners/banner_mob_4.webp")
    }
}

def download_file(fid, raw_path):
    # Always re-download to ensure we have the fresh updated version
    url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
    print(f"Downloading {os.path.basename(raw_path)} from Drive (id={fid})...")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if len(data) > 10000:
                    with open(raw_path, "wb") as f:
                        f.write(data)
                    sz_mb = len(data) / (1024 * 1024)
                    print(f"  Successfully downloaded {os.path.basename(raw_path)} ({sz_mb:.2f} MB)")
                    return True
                else:
                    print(f"  Attempt {attempt+1}: Data too small ({len(data)} bytes)")
        except Exception as e:
            print(f"  Attempt {attempt+1} error: {e}")
            time.sleep(2)
    return False

def convert_to_hd_webp(raw_path, dest_webp, quality=92):
    try:
        im = Image.open(raw_path)
        w, h = im.size
        orig_sz = os.path.getsize(raw_path) / (1024 * 1024)
        
        # Ensure RGBA / RGB handling
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im = im.convert('RGBA')
        else:
            im = im.convert('RGB')

        os.makedirs(os.path.dirname(dest_webp), exist_ok=True)
        im.save(dest_webp, 'WEBP', quality=quality, method=6)
        new_sz = os.path.getsize(dest_webp) / 1024
        
        print(f"  Converted {os.path.basename(dest_webp)}: {w}x{h} px | {orig_sz:.2f} MB -> {new_sz:.1f} KB (Quality {quality} HD)")
        return True
    except Exception as e:
        print(f"  Error converting {raw_path} to webp: {e}")
        return False

def main():
    print("=== Downloading and Converting Fresh Drive Assets ===\n")
    success_count = 0
    for key, info in TARGET_ASSETS.items():
        ok = download_file(info["id"], info["raw"])
        if ok:
            conv_ok = convert_to_hd_webp(info["raw"], info["dest"])
            if conv_ok:
                success_count += 1
        time.sleep(1)

    print(f"\nCompleted: {success_count} / {len(TARGET_ASSETS)} assets processed successfully!")

if __name__ == '__main__':
    main()


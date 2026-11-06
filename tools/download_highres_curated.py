import os
import urllib.request
import time

out_dir = 'scratch/curated_highres'
os.makedirs(out_dir, exist_ok=True)

targets = {
    # Hero Models
    'hero_1_heart_yellow_DSC02721.jpg': '1XluAqucr650Zxd1QxAZGqk5Qf5Zg5Dsf',
    'hero_2_pearl_blazer_DSC02810.jpg': '14ikVY9PH7B8OZank1tiSHG7GJNYR2s1h',
    'hero_3_tennis_green_DSC02915.jpg': '1PAU2XNa0IOZNK-vqmK8K3OE6DhrGRBe6',
    'hero_4_tiara_blazer_DSC02831.jpg': '1dfnZrwsA1OKmHTzxGDbJ_6uS5RXDQWV7',
    
    # Categories
    'cat_necklaces_DSC03100.jpg': '112AeyeBulHmrWGfIrCeSjBD7gA69eetM',
    'cat_rings_DSC03013.jpg': '1Xxs5b-xCKsdoRJoWwEtQ4dbAUG5olm7M',
    'cat_bracelets_DSC03087.jpg': '1Kyt7abKpgqzFR26J9pZ7wlEeZnj_roZe',
    'cat_earrings_DSC03001.jpg': '1cIUUVoCNYHlrAgWap-MRrpoUaa5atAgq',
    'cat_anklets_DSC03040.jpg': '1VaJRpEJHogAuz2CeXXBAgPF--6b0MVi-',
    'cat_suites_DSC03045.jpg': '1wKQD7B5DaFfw-svI1dQp4375p9hIhGBQ',
    
    # Curated Collections
    'col_links_layers_DSC03064.jpg': '17eFYNI0gr34KEEl_8feEzMvW0-AHXjHE',
    'col_drops_halo_DSC03109.jpg': '1tNR7B0NZjL5GHRBIIUCsgQYI9DuyLo0m',
    'col_dainty_steps_DSC03040.jpg': '1VaJRpEJHogAuz2CeXXBAgPF--6b0MVi-',
    'col_daily_luxe_DSC03116.jpg': '1gW-27hpBhxlwqNmmyLHqqtTqVB0p2OQ7',
    'col_tennis_fever_DSC03085.jpg': '1gpeaUYMg1B9GkfXcHLnHduVtjI2qcBPF',
    'col_heirloom_suites_DSC03070.jpg': '1UAUe5hWaSRB8hXda9eL3Ugxrnc4WV2w1',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print(f"Downloading {len(targets)} high-res curated assets from Drive...")

for fname, fid in targets.items():
    save_path = os.path.join(out_dir, fname)
    if os.path.exists(save_path) and os.path.getsize(save_path) > 50000:
        print(f"Already exists: {fname} ({os.path.getsize(save_path)/1024:.1f} KB)")
        continue
    
    url = f"https://lh3.googleusercontent.com/u/0/d/{fid}=w1600"
    try:
        t0 = time.time()
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded {fname}: {len(data)/1024:.1f} KB in {time.time()-t0:.2f}s")
    except Exception as e:
        print(f"Error downloading {fname}: {e}")
    time.sleep(0.3)

print("All curated high-res assets downloaded.")

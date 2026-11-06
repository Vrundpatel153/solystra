import os
import json
import time
import urllib.request
import psutil

out_dir = 'scratch/drive_thumbnails'
os.makedirs(out_dir, exist_ok=True)

with open('scratch/all_drive_jpgs.json', 'r', encoding='utf-8') as f:
    drive_data = json.load(f)

total = len(drive_data)
existing = [f for f in os.listdir(out_dir) if f.endswith('.jpg')]
print(f"Starting download of {total} thumbnails. Already downloaded: {len(existing)}")

downloaded = 0
failed = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for idx, (filename, file_id) in enumerate(drive_data.items(), 1):
    save_path = os.path.join(out_dir, filename)
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1000:
        continue
    
    url = f"https://lh3.googleusercontent.com/u/0/d/{file_id}=w350"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(save_path, 'wb') as out_f:
                    out_f.write(data)
                downloaded += 1
            else:
                failed += 1
            del data
    except Exception as e:
        failed += 1
    
    if idx % 25 == 0 or idx == total:
        avail = psutil.virtual_memory().available / (1024 * 1024)
        print(f"[{idx}/{total}] Downloaded: {downloaded}, Failed: {failed}, RAM Available: {avail:.0f} MB")
    
    time.sleep(0.05)

print(f"Finished. Total downloaded in this run: {downloaded}, failed: {failed}")


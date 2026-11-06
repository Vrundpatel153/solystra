import os
import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

out_dir = 'scratch/drive_thumbnails'
os.makedirs(out_dir, exist_ok=True)

with open('scratch/all_drive_jpgs.json', 'r', encoding='utf-8') as f:
    drive_data = json.load(f)

items_to_download = []
for filename, file_id in drive_data.items():
    save_path = os.path.join(out_dir, filename)
    if not os.path.exists(save_path) or os.path.getsize(save_path) < 1000:
        items_to_download.append((filename, file_id))

print(f"Total: {len(drive_data)}, To fetch: {len(items_to_download)}", flush=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_one(item):
    filename, file_id = item
    save_path = os.path.join(out_dir, filename)
    url = f"https://lh3.googleusercontent.com/u/0/d/{file_id}=w350"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = resp.read()
            if len(data) > 500:
                with open(save_path, 'wb') as f_out:
                    f_out.write(data)
                return True
    except Exception:
        pass
    return False

completed = 0
successes = 0
t0 = time.time()

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_one, item): item for item in items_to_download}
    for future in as_completed(futures):
        completed += 1
        if future.result():
            successes += 1
        if completed % 25 == 0 or completed == len(items_to_download):
            elapsed = time.time() - t0
            print(f"[{completed}/{len(items_to_download)}] Success: {successes}, Elapsed: {elapsed:.1f}s", flush=True)

print(f"Done. Successfully downloaded: {successes}/{len(items_to_download)} in {time.time()-t0:.1f}s", flush=True)


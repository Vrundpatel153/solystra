import os
import json
import urllib.request
import time

with open('scratch/all_drive_jpgs.json', 'r', encoding='utf-8') as f:
    jpg_map = json.load(f)

# Sort all keys
sorted_keys = sorted(jpg_map.keys())
print(f"Total keys: {len(sorted_keys)}")

# Sample 15 evenly spaced shots
step = len(sorted_keys) // 15
sample_keys = [sorted_keys[i * step] for i in range(15)]
if sorted_keys[-1] not in sample_keys:
    sample_keys.append(sorted_keys[-1])

out_dir = 'scratch/model_samples'
os.makedirs(out_dir, exist_ok=True)

for name in sample_keys:
    fid = jpg_map[name]
    dest = os.path.join(out_dir, name)
    if os.path.exists(dest):
        continue
    url = f"https://drive.google.com/thumbnail?id={fid}&sz=w600"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            with open(dest, 'wb') as f:
                f.write(data)
            print(f"Downloaded {name} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {name}: {e}")
    time.sleep(0.2)

print("Sample download finished!")


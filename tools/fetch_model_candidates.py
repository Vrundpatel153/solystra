import os
import json
import urllib.request
import time

with open('scratch/all_drive_jpgs.json', 'r', encoding='utf-8') as f:
    jpg_map = json.load(f)

candidates = [
    'DSC02714.JPG', 'DSC02715.JPG', 'DSC02716.JPG',
    'DSC02724.JPG', 'DSC02725.JPG', 'DSC02726.JPG',
    'DSC02744.JPG', 'DSC02745.JPG', 'DSC02747.JPG',
    'DSC02772.JPG', 'DSC02773.JPG',
    'DSC02821.JPG', 'DSC02822.JPG', 'DSC02823.JPG',
    'DSC02850.JPG', 'DSC02852.JPG'
]

out_dir = 'scratch/model_candidates'
os.makedirs(out_dir, exist_ok=True)

for name in candidates:
    if name not in jpg_map:
        continue
    fid = jpg_map[name]
    dest = os.path.join(out_dir, name)
    if os.path.exists(dest):
        continue
    url = f"https://drive.google.com/thumbnail?id={fid}&sz=w800"
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

print("Candidate download complete!")


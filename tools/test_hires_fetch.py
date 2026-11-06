import json
import urllib.request
import os

with open('scratch/all_drive_jpgs.json', 'r') as f:
    drive_data = json.load(f)

test_files = ['DSC02735.JPG', 'DSC02859.JPG', 'DSC02820.JPG', 'DSC02923.JPG']
for fn in test_files:
    fid = drive_data.get(fn)
    print(f"{fn} -> fid: {fid}")
    if fid:
        url = f"https://lh3.googleusercontent.com/u/0/d/{fid}=w1200"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
                print(f"  Successfully fetched {fn}: {len(data)} bytes ({resp.status})")
        except Exception as e:
            print(f"  Failed: {e}")

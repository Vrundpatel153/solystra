import re
import json

for idx in [1, 3]:
    with open(f"scratch/drive_ds_{idx}.txt", "r", encoding="utf-8") as f:
        c = f.read()
    print(f"=== Script {idx} (length {len(c)}) ===")
    strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', c)
    print(f"Total strings: {len(strings)}")
    for s in strings:
        if any(k in s.lower() for k in ['banner', 'category', 'collection', 'folder', 'image', 'hero', '1g8z', 'dsc', 'png', 'jpg', 'webp', 'pc', 'mobile', 'silver', 'quantrolab']):
            print(" ->", s)

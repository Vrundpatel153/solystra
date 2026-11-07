import os

js_dir = 'jewellery-design-html/js'
for f in os.listdir(js_dir):
    if f.endswith('.js'):
        p = os.path.join(js_dir, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
            for term in ["Click to view piece", "Shop Piece", "hotspot", "activeHotspot", "renderHotspots"]:
                if term in content:
                    print(f"Found '{term}' in {f}")

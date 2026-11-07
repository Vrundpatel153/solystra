import os

for root, _, files in os.walk('jewellery-design-html'):
    for f in files:
        if f.endswith(('.html', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                for kw in ['popover', 'tooltip', 'hotspot']:
                    if kw in c:
                        print(f"Found '{kw}' in {p}")

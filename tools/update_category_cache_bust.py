import os
import re

html_files = [
    'jewellery-design-html/index.html',
    'jewellery-design-html/categories.html',
    'jewellery-design-html/collections.html',
    'jewellery-design-html/products.html'
]

for fpath in html_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace zavya_style/*.webp?v=... with ?v=drive_curated_v1
    new_content = re.sub(r'(solystra_assets/categories/zavya_style/[a-zA-Z0-9_\.]+\.webp)(?:\?[^"\'\s>]*)?', r'\1?v=drive_curated_v1', content)
    # Also collections
    new_content = re.sub(r'(solystra_assets/collections/[a-zA-Z0-9_\.]+\.webp)(?:\?[^"\'\s>]*)?', r'\1?v=drive_curated_v1', new_content)
    
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated cache buster in {fpath}")

print("Cache bust applied!")


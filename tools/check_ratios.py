import os
import re
from PIL import Image

print("--- 1. Checking Product Card Container Classes in HTML/JS ---")
for file_path in ['jewellery-design-html/index.html', 'jewellery-design-html/products.html', 'jewellery-design-html/js/app.js']:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # find product card image container snippets
            matches = re.findall(r'(<div[^>]*aspect-[^>]*>|<img[^>]*aspect-[^>]*>)', content)
            print(f"\nIn {file_path}:")
            for m in matches[:10]:
                print("  ", m[:120])
            
            # find product card template in js
            card_snippets = re.findall(r'aspect-[a-zA-Z0-9\-\/\[\]]+', content)
            print("   Unique aspect-* classes:", set(card_snippets))

print("\n--- 2. Checking Rendered Product Card Snippet in JS ---")
if os.path.exists('jewellery-design-html/js/app.js'):
    with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()
        # Find where product cards are generated
        for line in app_js.split('\n'):
            if 'aspect-' in line or 'product-card' in line or 'product_image' in line or 'createProductCard' in line or 'renderCatalog' in line:
                if len(line.strip()) < 180:
                    print("  ", line.strip())

print("\n--- 3. Checking Actual Product Image Dimensions on Disk ---")
# Check products images in assets/ or wherever product images are stored
image_dirs = [
    'jewellery-design-html/assets/images/products',
    'jewellery-design-html/assets/products',
    'jewellery-design-html/assets/images',
    'jewellery-design-html/images',
    'jewellery-design-html/assets'
]

checked = 0
ratio_counts = {}

for root, dirs, files in os.walk('jewellery-design-html'):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif')):
            # filter for product images
            full_path = os.path.join(root, file)
            # check if it looks like a product image
            if 'product' in root.lower() or 'catalog' in root.lower() or 'jewellery' in root.lower() or 'items' in root.lower() or 'ring' in file.lower() or 'necklace' in file.lower() or 'bracelet' in file.lower() or 'earring' in file.lower():
                try:
                    with Image.open(full_path) as img:
                        w, h = img.size
                        ratio = round(w / h, 2)
                        ratio_str = f"{w}x{h} (ratio {ratio})"
                        ratio_counts[ratio] = ratio_counts.get(ratio, 0) + 1
                        checked += 1
                        if checked <= 15:
                            print(f"Sample: {file} -> {w}x{h} ({ratio}:1)")
                except Exception as e:
                    pass

print(f"\nTotal product images sampled: {checked}")
print("Ratio distribution (width / height):")
for r, count in sorted(ratio_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  Ratio ~{r}:1 -> {count} images")


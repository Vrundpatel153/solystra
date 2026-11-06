import os
from PIL import Image
from collections import Counter

folder = 'jewellery-design-html/solystra_assets/products'
ratios = []
details = []

for root, dirs, files in os.walk(folder):
    for f in files:
        if f.lower().endswith(('.webp', '.jpg', '.png', '.jpeg')):
            full_path = os.path.join(root, f)
            try:
                with Image.open(full_path) as img:
                    w, h = img.size
                    # classify ratio
                    r = w / h
                    if 0.95 <= r <= 1.05:
                        cat = "1:1 Square"
                    elif 0.77 <= r <= 0.83:
                        cat = "4:5 Portrait (0.80)"
                    elif 0.72 <= r <= 0.76:
                        cat = "3:4 Portrait (0.75)"
                    elif 0.64 <= r <= 0.70:
                        cat = "2:3 Portrait (0.67)"
                    elif 0.85 <= r <= 0.94:
                        cat = "Near-square / Slight Portrait (0.85 - 0.94)"
                    elif 1.06 <= r <= 1.20:
                        cat = "Slight Landscape (1.1 - 1.2)"
                    elif 1.21 <= r <= 1.40:
                        cat = "4:3 Landscape (1.33)"
                    elif 1.41 <= r <= 1.60:
                        cat = "3:2 Landscape (1.50)"
                    else:
                        cat = f"Other ({round(r, 2)}:1)"
                    
                    ratios.append(cat)
                    details.append((f, w, h, round(r, 3)))
            except Exception as e:
                pass

print(f"Total product images analyzed in {folder}: {len(ratios)}")
counts = Counter(ratios)
for cat, count in counts.most_common():
    pct = round(count / len(ratios) * 100, 1)
    print(f"  {cat}: {count} files ({pct}%)")

print("\nCommon pixel dimensions:")
dim_counts = Counter([f"{w}x{h}" for _, w, h, _ in details])
for dim, count in dim_counts.most_common(8):
    print(f"  {dim}: {count} files")


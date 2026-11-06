import os
import re

print("=== CHECKING CATEGORIES.HTML CATEGORY CARDS ===")
with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    cat_html = f.read()

# find category cards or img tags
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', cat_html)
print(f"Found {len(imgs)} img tags in categories.html:")
for img in imgs[:15]:
    print(" ", img)

# find text like "Designs ("
designs_matches = re.findall(r'(\w+[\s\w&]*?)\s*</h3>[\s\S]*?(\d+\s*Designs)', cat_html)
print("\nCard titles and counts:")
for d in designs_matches[:10]:
    print(" ", d)

print("\n=== CHECKING PRODUCTS.HTML FILTER CODE ===")
with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    prod_html = f.read()

# search for mobile-filter-drawer
drawer_match = re.search(r'id=["\']mobile-filter-drawer["\'][\s\S]*?</aside>', prod_html)
if drawer_match:
    print("Found mobile-filter-drawer in products.html, length:", len(drawer_match.group(0)))
else:
    print("No mobile-filter-drawer found in products.html")

# search for "curated" in index.html
with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

curated_matches = [m.start() for m in re.finditer(r'curated', idx_html, re.I)]
print(f"Found {len(curated_matches)} occurrences of 'curated' in index.html")
for pos in curated_matches[:5]:
    print("---", idx_html[max(0, pos-80):pos+120], "---")


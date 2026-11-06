import re
from PIL import Image
import os

print("=== 1. Products.html Card Markup ===")
with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    p_html = f.read()

grid_idx = p_html.find('id="products-catalog-grid"')
if grid_idx != -1:
    print(p_html[grid_idx:grid_idx+1200])

print("\n=== 2. Index.html Product Card Markup ===")
with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    i_html = f.read()

# search for product card sections (e.g. Best Sellers, Trending, etc.)
product_cards = re.findall(r'<div[^>]*class="[^"]*group[^"]*"[^>]*>.*?<img[^>]*>.*?</div>', i_html, re.DOTALL)
for pc in product_cards[:3]:
    print("Found Card in index.html:")
    print(pc[:400])

print("\n=== 3. Product Images in Catalog vs Index ===")
# Find all img src in products-catalog-grid
img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', p_html)
print(f"Total img tags in products.html: {len(img_srcs)}")

# Sample product images from products.html and check their actual dimensions
catalog_dims = []
for src in img_srcs[:25]:
    # resolve path
    local_src = src.lstrip('/')
    full_path = os.path.join('jewellery-design-html', local_src)
    if os.path.exists(full_path):
        try:
            with Image.open(full_path) as img:
                catalog_dims.append((src, img.size, round(img.size[0] / img.size[1], 3)))
        except:
            pass

print("\nSample images in products.html:")
for src, (w, h), r in catalog_dims[:15]:
    print(f"  {src} -> {w}x{h} (Ratio {r}:1 or {round(h/w, 3)}:1 portrait)")

print("\n=== 4. Product Details / Product Modal in product.html ===")
if os.path.exists('jewellery-design-html/product.html'):
    with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
        prod_page = f.read()
    prod_imgs = re.findall(r'<div[^>]*aspect-[^>]*>', prod_page)
    print("Aspect ratios in product.html:", prod_imgs)


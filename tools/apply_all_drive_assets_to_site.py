import os
import re

index_path = os.path.abspath('jewellery-design-html/index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Head Preloads
html = re.sub(
    r'<link rel="preload" as="image" href="[^"]*banner[^"]*" media="\(min-width: 641px\)" fetchpriority="high"/>',
    '<link rel="preload" as="image" href="solystra_assets/banners/banner_pc_1.webp?v=drive2026" media="(min-width: 641px)" fetchpriority="high"/>',
    html
)
html = re.sub(
    r'<link rel="preload" as="image" href="[^"]*banner[^"]*" media="\(max-width: 640px\)" fetchpriority="high"/>',
    '<link rel="preload" as="image" href="solystra_assets/banners/banner_mob_1.webp?v=drive2026" media="(max-width: 640px)" fetchpriority="high"/>',
    html
)

# 2. Update Hero Banner Slide 0 (banner 1 PC & Mobile)
slide_0_old = re.search(r'(<div[^>]*data-hero-slide="0"[^>]*>.*?<picture>)(.*?)(</picture>)', html, re.DOTALL)
if slide_0_old:
    new_pic_0 = '<source media="(max-width: 640px)" srcset="solystra_assets/banners/banner_mob_1.webp?v=drive2026"/><img alt="The 18K Gold Suite" class="w-full h-full object-cover object-center block" loading="eager" fetchpriority="high" src="solystra_assets/banners/banner_pc_1.webp?v=drive2026"/>'
    html = html.replace(slide_0_old.group(0), slide_0_old.group(1) + new_pic_0 + slide_0_old.group(3))
    print("Updated Hero Slide 0 with banner-1-pc and banner-1-mobile!")

# 3. Update Hero Banner Slide 1 (banner 2 PC & Mobile)
slide_1_old = re.search(r'(<div[^>]*data-hero-slide="1"[^>]*>.*?<picture>)(.*?)(</picture>)', html, re.DOTALL)
if slide_1_old:
    new_pic_1 = '<source media="(max-width: 640px)" srcset="solystra_assets/banners/banner_mob_2.webp?v=drive2026"/><img alt="Blush Tones Collection" class="w-full h-full object-cover object-center block" loading="lazy" src="solystra_assets/banners/banner_pc_2.webp?v=drive2026"/>'
    html = html.replace(slide_1_old.group(0), slide_1_old.group(1) + new_pic_1 + slide_1_old.group(3))
    print("Updated Hero Slide 1 with banner-2-pc and banner2-mobile!")

# 4. Update Hero Banner Slide 2 (Floral Portrait PC & Mobile)
slide_2_old = re.search(r'(<div[^>]*data-hero-slide="2"[^>]*>.*?<picture>)(.*?)(</picture>)', html, re.DOTALL)
if slide_2_old:
    new_pic_2 = '<source media="(max-width: 640px)" srcset="solystra_assets/banners/banner_floral_portrait_mob.webp?v=drive2026"/><img alt="Modern Classics" class="w-full h-full object-cover object-center block" loading="lazy" src="solystra_assets/banners/banner_floral_portrait.webp?v=drive2026"/>'
    html = html.replace(slide_2_old.group(0), slide_2_old.group(1) + new_pic_2 + slide_2_old.group(3))
    print("Updated Hero Slide 2 with Floral Portrait PC & Mobile!")

# 5. Update Hero Banner Slide 3 (Profile Floral PC & Mobile)
slide_3_old = re.search(r'(<div[^>]*data-hero-slide="3"[^>]*>.*?<picture>)(.*?)(</picture>)', html, re.DOTALL)
if slide_3_old:
    new_pic_3 = '<source media="(max-width: 640px)" srcset="solystra_assets/banners/banner_profile_floral_mob.webp?v=drive2026"/><img alt="Signature Gift Sets" class="w-full h-full object-cover object-center block" loading="lazy" src="solystra_assets/banners/banner_profile_floral.webp?v=drive2026"/>'
    html = html.replace(slide_3_old.group(0), slide_3_old.group(1) + new_pic_3 + slide_3_old.group(3))
    print("Updated Hero Slide 3 with Profile Floral PC & Mobile!")

# 6. Update Curated Collections cards in index.html
# Replace old sources with new drive_curated collection images
html = html.replace('solystra_assets/categories/zavya_style/chains.webp?v=authentic_products_v2', 'solystra_assets/drive_curated/collection_links.webp?v=drive2026')
html = html.replace('solystra_assets/collections/collection_drops.webp?v=authentic_products_v2', 'solystra_assets/drive_curated/collection_drops.webp?v=drive2026')
html = html.replace('solystra_assets/drive_curated/collection_dainty.webp?v=drive_curated_v1', 'solystra_assets/drive_curated/collection_dainty.webp?v=drive2026')
html = html.replace('solystra_assets/drive_curated/collection_ombre.webp?v=drive_curated_v1', 'solystra_assets/drive_curated/collection_daily_luxe.webp?v=drive2026')
html = html.replace('solystra_assets/drive_curated/collection_tennis.webp?v=drive_curated_v1', 'solystra_assets/drive_curated/collection_tennis.webp?v=drive2026')

# 7. Update Category section cache busters in index.html
for cat in ['necklaces.webp', 'earrings.webp', 'bracelets.webp', 'rings.webp', 'anklets.webp', 'complete_sets.webp']:
    html = re.sub(rf'solystra_assets/drive_curated/{cat}(?:\?v=[a-zA-Z0-9_-]+)?', f'solystra_assets/drive_curated/{cat}?v=drive2026', html)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated with all Drive category, collection, and banner assets!")

# Also update categories.html
cat_html_path = os.path.abspath('jewellery-design-html/categories.html')
if os.path.exists(cat_html_path):
    with open(cat_html_path, 'r', encoding='utf-8') as f:
        cat_c = f.read()
    for cat in ['necklaces.webp', 'earrings.webp', 'bracelets.webp', 'rings.webp', 'anklets.webp', 'complete_sets.webp']:
        cat_c = re.sub(rf'solystra_assets/drive_curated/{cat}(?:\?v=[a-zA-Z0-9_-]+)?', f'solystra_assets/drive_curated/{cat}?v=drive2026', cat_c)
    with open(cat_html_path, 'w', encoding='utf-8') as f:
        f.write(cat_c)
    print("categories.html updated!")

# Also update catalog.js
cat_js_path = os.path.abspath('jewellery-design-html/js/catalog.js')
if os.path.exists(cat_js_path):
    with open(cat_js_path, 'r', encoding='utf-8') as f:
        js_c = f.read()
    for cat in ['necklaces.webp', 'earrings.webp', 'bracelets.webp', 'rings.webp', 'anklets.webp', 'complete_sets.webp']:
        js_c = re.sub(rf'solystra_assets/drive_curated/{cat}(?:\?v=[a-zA-Z0-9_-]+)?', f'solystra_assets/drive_curated/{cat}?v=drive2026', js_c)
    with open(cat_js_path, 'w', encoding='utf-8') as f:
        f.write(js_c)
    print("catalog.js updated!")


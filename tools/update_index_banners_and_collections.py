with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace slide 3 banners
content = content.replace(
    'solystra_assets/banners/banner_floral_portrait_mob.webp?v=drive2026',
    'solystra_assets/banners/banner_mob_3.webp?v=drive2026_v2'
)
content = content.replace(
    'solystra_assets/banners/banner_floral_portrait.webp?v=drive2026',
    'solystra_assets/banners/banner_pc_3.webp?v=drive2026_v2'
)

# Replace slide 4 banners
content = content.replace(
    'solystra_assets/banners/banner_profile_floral_mob.webp?v=drive2026',
    'solystra_assets/banners/banner_mob_4.webp?v=drive2026_v2'
)
content = content.replace(
    'solystra_assets/banners/banner_profile_floral.webp?v=drive2026',
    'solystra_assets/banners/banner_pc_4.webp?v=drive2026_v2'
)

# Update cache buster on slide 1 and 2
content = content.replace('banner_mob_1.webp?v=drive2026', 'banner_mob_1.webp?v=drive2026_v2')
content = content.replace('banner_pc_1.webp?v=drive2026', 'banner_pc_1.webp?v=drive2026_v2')
content = content.replace('banner_mob_2.webp?v=drive2026', 'banner_mob_2.webp?v=drive2026_v2')
content = content.replace('banner_pc_2.webp?v=drive2026', 'banner_pc_2.webp?v=drive2026_v2')

# Update cache buster on collections
for name in ['collection_links', 'collection_drops', 'collection_dainty', 'collection_daily_luxe', 'collection_tennis']:
    content = content.replace(f'{name}.webp?v=drive2026', f'{name}.webp?v=drive2026_v2')

with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html updated successfully!")


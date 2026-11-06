with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace category images in category carousel
# Note: Keep the header showcase as-is or replace category loops
# In the category section:
# Look for category buttons
cat_map = {
    'solystra_assets/categories/zavya_style/necklaces.webp?v=authentic_products_v2': 'solystra_assets/drive_curated/necklaces.webp?v=drive_curated_v1',
    'solystra_assets/categories/zavya_style/earrings.webp?v=authentic_products_v2': 'solystra_assets/drive_curated/earrings.webp?v=drive_curated_v1',
    'solystra_assets/categories/zavya_style/bracelets.webp?v=authentic_products_v2': 'solystra_assets/drive_curated/bracelets.webp?v=drive_curated_v1',
    'solystra_assets/categories/zavya_style/rings.webp?v=authentic_products_v2': 'solystra_assets/drive_curated/rings.webp?v=drive_curated_v1',
    'solystra_assets/categories/zavya_style/anklets.webp?v=authentic_products_v2': 'solystra_assets/drive_curated/anklets.webp?v=drive_curated_v1',
    'solystra_assets/categories/zavya_style/complete_sets.webp?v=authentic_products_v2': 'solystra_assets/drive_curated/complete_sets.webp?v=drive_curated_v1',
}

# In collection carousel:
# Note: collection cards have alt="Links & Layers", alt="Drops & Halo", alt="Dainty Steps", alt="Daily Luxe", alt="Tennis Fever"
import re

def replace_collection_card(match):
    full_card = match.group(0)
    if 'alt="Links & Layers"' in full_card:
        full_card = re.sub(r'src="[^"]+"', 'src="solystra_assets/drive_curated/collection_links.webp?v=drive_curated_v1"', full_card)
    elif 'alt="Drops & Halo"' in full_card:
        full_card = re.sub(r'src="[^"]+"', 'src="solystra_assets/drive_curated/collection_drops.webp?v=drive_curated_v1"', full_card)
    elif 'alt="Dainty Steps"' in full_card:
        full_card = re.sub(r'src="[^"]+"', 'src="solystra_assets/drive_curated/collection_dainty.webp?v=drive_curated_v1"', full_card)
    elif 'alt="Daily Luxe"' in full_card:
        full_card = re.sub(r'src="[^"]+"', 'src="solystra_assets/drive_curated/collection_ombre.webp?v=drive_curated_v1"', full_card)
    elif 'alt="Tennis Fever"' in full_card:
        full_card = re.sub(r'src="[^"]+"', 'src="solystra_assets/drive_curated/collection_tennis.webp?v=drive_curated_v1"', full_card)
    return full_card

# Apply category replacements
for old_s, new_s in cat_map.items():
    cnt = content.count(old_s)
    print(f"Replacing {old_s}: {cnt} occurrences")
    content = content.replace(old_s, new_s)

# Apply collection replacements
pattern = r'<div[^>]*data-collection-card="true"[^>]*>[\s\S]*?<\/div>\s*<\/div>'
matches = re.findall(pattern, content)
print(f"Found {len(matches)} collection cards to update")

content = re.sub(pattern, replace_collection_card, content)

with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html with Drive curated assets successfully!")

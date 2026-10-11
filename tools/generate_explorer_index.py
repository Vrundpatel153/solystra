"""
generate_explorer_index.py
Compiles an index of all downloaded local media (banners, branding, product photos, HD videos)
into zavya_assets/metadata/downloaded_media_index.json for instant browsing in asset_explorer.html
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'zavya_assets')
METADATA_DIR = os.path.join(ASSETS_DIR, 'metadata')

def main():
    items = []

    # 1. Site banners
    banners_dir = os.path.join(ASSETS_DIR, 'site_banners')
    if os.path.exists(banners_dir):
        for f in sorted(os.listdir(banners_dir)):
            if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                items.append({
                    'category': 'Site Banners',
                    'sub_category': 'Homepage & Promos',
                    'title': f,
                    'type': 'image',
                    'path': f"site_banners/{f}",
                    'size': os.path.getsize(os.path.join(banners_dir, f))
                })

    # 2. Branding
    branding_dir = os.path.join(ASSETS_DIR, 'branding')
    if os.path.exists(branding_dir):
        for f in sorted(os.listdir(branding_dir)):
            if any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif']):
                items.append({
                    'category': 'Branding',
                    'sub_category': 'Logos & Trust Badges',
                    'title': f,
                    'type': 'image',
                    'path': f"branding/{f}",
                    'size': os.path.getsize(os.path.join(branding_dir, f))
                })

    # 3. Products
    products_dir = os.path.join(ASSETS_DIR, 'products')
    if os.path.exists(products_dir):
        for cat in sorted(os.listdir(products_dir)):
            cat_path = os.path.join(products_dir, cat)
            if not os.path.isdir(cat_path):
                continue
            for handle in sorted(os.listdir(cat_path)):
                handle_path = os.path.join(cat_path, handle)
                if not os.path.isdir(handle_path):
                    continue
                # Read product_info.json if exists
                title = handle.replace('-', ' ').title()
                pinfo_path = os.path.join(handle_path, 'product_info.json')
                price = None
                if os.path.exists(pinfo_path):
                    try:
                        with open(pinfo_path, 'r', encoding='utf-8') as pf:
                            info = json.load(pf)
                            title = info.get('title', title)
                            price = info.get('price')
                    except Exception:
                        pass

                for f in sorted(os.listdir(handle_path)):
                    fp = os.path.join(handle_path, f)
                    if f.lower().endswith('.mp4'):
                        items.append({
                            'category': 'Products',
                            'sub_category': cat.replace('_', ' ').title(),
                            'product_title': title,
                            'title': f"{title} (1080p Video)",
                            'price': price,
                            'type': 'video',
                            'path': f"products/{cat}/{handle}/{f}",
                            'size': os.path.getsize(fp)
                        })
                    elif any(f.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        items.append({
                            'category': 'Products',
                            'sub_category': cat.replace('_', ' ').title(),
                            'product_title': title,
                            'title': f"{title} ({f[:2]})",
                            'price': price,
                            'type': 'image',
                            'path': f"products/{cat}/{handle}/{f}",
                            'size': os.path.getsize(fp)
                        })

    out_file = os.path.join(METADATA_DIR, 'downloaded_media_index.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)

    total_size = sum(i['size'] for i in items)
    print(f"Generated downloaded media index: {len(items)} items ({total_size / (1024*1024):.2f} MB)")
    print(f"Images: {sum(1 for i in items if i['type'] == 'image')}")
    print(f"Videos: {sum(1 for i in items if i['type'] == 'video')}")
    print(f"Saved to: {out_file}")

if __name__ == '__main__':
    main()

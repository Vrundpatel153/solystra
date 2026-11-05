import os
import re
from bs4 import BeautifulSoup

def update_categories_html(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (does not exist)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    cat_mapping = {
        'bracelets & kadas': 'bracelets',
        'necklaces & pendants': 'necklaces',
        'rings & bands': 'rings',
        'earrings & studs': 'earrings',
        'gift suites & sets': 'complete_sets',
        'classic layering chains': 'chains',
        'anklets & payals': 'anklets',
        'sacred mangalsutras': 'mangalsutras',
        'solitaire nose pins': 'nose_pins',
        "men's silver collection": 'mens',
        "men’s silver collection": 'mens',
    }

    # 1. Update Explore All Catalog button
    for btn in soup.find_all('button'):
        if 'Explore All Catalog' in btn.text:
            btn['onclick'] = "window.location.href='products.html'"

    # 2. Update category cards
    count = 0
    for h3 in soup.find_all('h3'):
        title = h3.text.strip().lower()
        if title in cat_mapping:
            slug = cat_mapping[title]
            card = h3.find_parent('div', class_=lambda c: c and 'group' in c)
            if card:
                card['onclick'] = f"window.location.href='products.html?category={slug}'"
                card['role'] = 'link'
                card['tabindex'] = '0'
                card['onkeydown'] = f"if(event.key==='Enter'||event.key===' ')window.location.href='products.html?category={slug}'"
                
                # Cache bust image src
                img = card.find('img')
                if img and img.get('src'):
                    base_src = img['src'].split('?')[0]
                    img['src'] = f"{base_src}?v=atelier2026_v8"
                count += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Updated {filepath} ({count} cards wired)")

def update_index_html(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (does not exist)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. Fix Earrings pointing to rings
    earrings_fixed = 0
    for card in soup.find_all(attrs={'onclick': True}):
        oc = card['onclick']
        text = card.get_text().strip()
        if 'Earrings' in text and 'category=rings' in oc:
            card['onclick'] = "window.location.href='products.html?category=earrings'"
            earrings_fixed += 1

    # 2. Cache-bust all category and collection images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if 'zavya_style' in src or 'collections/' in src:
            base_src = src.split('?')[0]
            img['src'] = f"{base_src}?v=atelier2026_v8"

    # 3. Wire Top Collections coverflow cards
    top_coll_mapping = {
        'chains & necklaces': "window.location.href='products.html?category=chains'",
        'rings & earrings': "window.location.href='products.html?category=rings'",
        'anklets & payals': "window.location.href='products.html?category=anklets'",
        '18k gold products': "window.location.href='products.html?metal=gold'",
        'tennis bracelets': "window.location.href='products.html?category=bracelets'",
    }

    wired_colls = 0
    for sec in soup.find_all('section'):
        h2 = sec.find(['h2', 'h3'])
        if h2 and 'Top Collections' in h2.text:
            cards = sec.find_all('div', class_=lambda c: c and ('collection-card' in c or 'group' in c))
            for card in cards:
                text = card.get_text().strip().lower()
                for key, action in top_coll_mapping.items():
                    if key in text:
                        card['onclick'] = action
                        card['role'] = 'link'
                        card['tabindex'] = '0'
                        card['style'] = (card.get('style', '') + '; cursor: pointer;').strip(';')
                        wired_colls += 1
                        break

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Updated {filepath} (Fixed {earrings_fixed} earrings, wired {wired_colls} collections)")

# Run for all targets
targets = [
    ('jewellery-design-html/categories.html', 'jewellery-design-html/index.html'),
    ('jewellery-design-html-dist/categories.html', 'jewellery-design-html-dist/index.html'),
    (r'c:\Users\vrund\OneDrive\Desktop\solystra-html\categories.html', r'c:\Users\vrund\OneDrive\Desktop\solystra-html\index.html'),
]

for cat_file, idx_file in targets:
    update_categories_html(cat_file)
    update_index_html(idx_file)

print("All card redirections applied successfully across all targets!")


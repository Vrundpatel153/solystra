from bs4 import BeautifulSoup
import re

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
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

# 1. Update Explore All button
for btn in soup.find_all('button'):
    if 'Explore All Catalog' in btn.text:
        btn['onclick'] = "window.location.href='products.html'"
        print("Wired Explore All Catalog button")

# 2. Update category cards
updated_cards = 0
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
            
            updated_cards += 1
            print(f"Wired card: {title} -> products.html?category={slug}")

print(f"Total cards wired: {updated_cards}")


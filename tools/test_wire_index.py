from bs4 import BeautifulSoup
import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# 1. Update Explore by Category
fixed_earrings = 0
for card in soup.find_all(attrs={'onclick': True}):
    oc = card['onclick']
    # Check if card is Earrings but points to rings
    text = card.get_text().strip()
    if 'Earrings' in text and 'category=rings' in oc:
        card['onclick'] = "window.location.href='products.html?category=earrings'"
        fixed_earrings += 1
print(f"Fixed {fixed_earrings} Earrings cards pointing to rings.")

# Cache-bust all category images in index.html
for img in soup.find_all('img'):
    src = img.get('src', '')
    if 'zavya_style' in src or 'collections/' in src:
        base_src = src.split('?')[0]
        img['src'] = f"{base_src}?v=atelier2026_v8"

# 2. Wire Top Collections coverflow cards
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

print(f"Wired {wired_colls} collection cards in Top Collections.")


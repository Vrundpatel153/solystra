with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find all id attributes
ids = re.findall(r'id=["\']([^"\']+)["\']', text)
print('IDs related to product/grid/catalog:', [i for i in ids if any(k in i.lower() for k in ['product', 'grid', 'catalog', 'card', 'list'])])

grid_idx = text.find('id="products-catalog-grid"')
if grid_idx != -1:
    grid_end = text.find('</main>', grid_idx)
    grid_content = text[grid_idx:grid_end]
    cards = re.findall(r'<div class="group bg-white rounded-2xl', grid_content)
    print(f'Total product cards inside grid: {len(cards)}')
    
    # check if each card has data attributes (category, metal, price, etc.)
    card_samples = re.findall(r'<div class="group bg-white rounded-2xl[^>]*onclick="window\.location\.href=\'product\.html\?id=([^\']+)\'\"([^>]*)>', grid_content)
    print(f'Card sample ids (first 5): {[c[0] for c in card_samples[:5]]}')
    print(f'Card sample attributes: {card_samples[0][1]}')

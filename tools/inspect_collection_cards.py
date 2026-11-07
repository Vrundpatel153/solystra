with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# find all collection card elements
cards = re.findall(r'<div[^>]*data-collection-card="true"[^>]*>.*?</div>\s*</div>\s*</div>', c, re.DOTALL)
print(f"Found {len(cards)} collection cards:")
for idx, card in enumerate(cards[:10]):
    alt = re.search(r'alt="([^"]*)"', card)
    src = re.search(r'src="([^"]*)"', card)
    title = re.search(r'<h3[^>]*>([^<]+)</h3>', card)
    print(f"Card {idx}: Title={title.group(1) if title else 'none'} | alt={alt.group(1) if alt else 'none'} | src={src.group(1) if src else 'none'}")


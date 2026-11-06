with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'products-catalog-grid', text)]
print("Found matches for products-catalog-grid:", len(matches))
for pos in matches:
    print("Match at:", pos)
    print(text[max(0, pos-200):min(len(text), pos+600)])
    print("="*60)


with open('jewellery-design-html/js/catalog.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'golden-meadow', text, re.IGNORECASE)]
print("golden-meadow matches:", len(matches))
for idx in matches:
    print(text[max(0, idx-100):min(len(text), idx+600)])


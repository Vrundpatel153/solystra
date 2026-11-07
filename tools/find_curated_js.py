with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'curated', text, re.IGNORECASE)]
print("Curated matches in app.js:", len(matches))
for idx in matches[:10]:
    print(f"At {idx}:")
    print(text[max(0, idx-50):min(len(text), idx+200)])


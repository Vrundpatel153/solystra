with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find hotspot tooltip or hotspot markup in index.html
matches = re.findall(r'<div[^>]*class="[^"]*hotspot[^"]*"[^>]*>.*?</div>', text, re.DOTALL)
print(f"Hotspot matches in HTML: {len(matches)}")
for m in matches[:5]:
    print(m[:300])
    print("-" * 40)

# Also check for 'Shop Piece' or 'Click to view piece'
for phrase in ["Click to view piece", "Shop Piece", "hotspot-card", "hotspot-tooltip", "active-hotspot", "curated-looks"]:
    pos = 0
    found = 0
    while True:
        pos = text.find(phrase, pos)
        if pos == -1:
            break
        print(f"Found '{phrase}' in index.html at {pos}:")
        print(text[max(0, pos-150):min(len(text), pos+200)])
        print("=" * 50)
        pos += len(phrase)
        found += 1
        if found >= 3:
            break

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find hero slides
print("=== HERO SECTION IMAGES ===")
hero_matches = re.findall(r'<picture>.*?</picture>', text, re.DOTALL)
for i, m in enumerate(hero_matches[:8]):
    print(f"Picture {i+1}:")
    print(m.strip())
    print("-" * 40)

print("\n=== COLLECTION CARDS ===")
for m in re.finditer(r'collection_[a-zA-Z0-9_\-]+\.webp[^\"]*', text):
    print(m.group(0))


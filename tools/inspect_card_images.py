import re

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find card blocks
cards = re.findall(r'<div class="group bg-white rounded-2xl.*?(?=<div class="group bg-white rounded-2xl|</div>\s*</section>)', c, re.DOTALL)
print(f"Cards found: {len(cards)}")
for i, card in enumerate(cards):
    title_m = re.search(r'<h3[^>]*>(.*?)</h3>', card)
    title = title_m.group(1) if title_m else "No title"
    img_m = re.search(r'<img[^>]*src="([^"]*)"', card)
    img = img_m.group(1) if img_m else "No img"
    print(f"Card {i+1}: {title} -> {img}")


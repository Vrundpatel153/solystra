import re

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check cards
cards = re.findall(r'<div[^>]*data-id=["\']([^"\']+)["\'][^>]*>', html)
print(f"Found {len(cards)} data-id cards in products.html")


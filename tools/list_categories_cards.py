import re

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find all headings h3 or card titles
cards = re.findall(r'<h3[^>]*>(.*?)</h3>', c)
print(f"Total card titles in categories.html: {len(cards)}")
for i, title in enumerate(cards):
    print(f" {i+1}. {title}")


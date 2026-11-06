import re

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== CHECKING ONCLICK IN PRODUCTS.HTML ===")
for m in re.finditer(r'onclick=["\']([^"\']+)["\']', html):
    val = m.group(1)
    line = html[:m.start()].count('\n') + 1
    if any(k in val.lower() for k in ['filter', 'category', 'metal', 'search', 'location.href']):
        print(f"L{line}: {val}")

# Also check how script tag is loaded in products.html
script_tags = re.findall(r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>', html)
print("\nScript tags in products.html:", script_tags)


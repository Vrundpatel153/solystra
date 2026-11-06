import re

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

ids = re.findall(r'id=["\']([^"\']*(?:modal|drawer|filter|popup)[^"\']*)["\']', text, re.IGNORECASE)
print("Matching IDs:", set(ids))

# Check functions in app.js related to modal
with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

funcs = re.findall(r'window\.([a-zA-Z0-9_]*(?:filter|modal|popup|sort|catalog)[a-zA-Z0-9_]*)', app_js, re.IGNORECASE)
print("app.js matching window functions:", set(funcs))


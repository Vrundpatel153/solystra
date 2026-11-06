with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Check for "Collections" megamenu in index.html
pos = html.find('Explore All Categories Archive')
print("Found 'Explore All Categories Archive':", pos != -1)
if pos != -1:
    print("Snippet around 'Explore All Categories Archive':\n", html[pos-200:pos+800])

# Check for "All Products" or similar redirect in the megamenu
pos2 = html.find('products.html')
print("Found 'products.html':", pos2 != -1)
matches = re.findall(r'<a[^>]*href=\"products\.html\"[^>]*>.*?</a>', html, re.DOTALL)
print("Links to products.html:", len(matches))
for m in matches[:5]:
    print("  ->", m.strip())

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Find all divs with max-w or container or px before products-catalog-grid
pos = html.find('id="products-catalog-grid"')
# Let's inspect the 5000 chars before pos and print open divs
snippet = html[max(0, pos-5000):pos]
divs = re.findall(r'<div[^>]*>', snippet)
for d in divs[-15:]:
    print(d)


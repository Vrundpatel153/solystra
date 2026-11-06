with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

print("Length of products.html:", len(html))
main_match = re.search(r'<main[^>]*>', html)
if main_match:
    print("Main tag:", main_match.group(0))
    start = main_match.start()
    print("Main content snippet:\n", html[start:start+2500])

grid_match = re.search(r'<div[^>]*id="product[^"]*"[^>]*>', html)
if grid_match:
    print("Grid tag:", grid_match.group(0))

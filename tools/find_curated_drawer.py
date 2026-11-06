import os
import re

files = [
    'jewellery-design-html/index.html',
    'jewellery-design-html/products.html',
    'jewellery-design-html/categories.html',
    'jewellery-design-html/offers.html',
    'jewellery-design-html/product.html',
    'jewellery-design-html/checkout.html'
]

for fn in files:
    if os.path.exists(fn):
        with open(fn, 'r', encoding='utf-8') as f:
            c = f.read()
        pos = c.find('Curated Collections')
        print(f"{fn}:")
        count = 0
        while pos != -1:
            count += 1
            is_mobile = 'lg:hidden' in c[max(0, pos-800):pos]
            print(f"  Match {count} at {pos} (mobile context: {is_mobile})")
            pos = c.find('Curated Collections', pos+1)


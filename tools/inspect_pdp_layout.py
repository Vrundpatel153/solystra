with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find main content / grid
pos_main = html.find('<main')
pos_end = html.find('SPECIFICATIONS & PURITY')

print("Main to Specifications snippet:\n")
print(html[pos_main:pos_main+2000])

# Let's see the column definitions
grid_pos = html.find('grid lg:grid-cols', pos_main)
if grid_pos == -1:
    grid_pos = html.find('grid-cols', pos_main)
print("\nGrid section:\n", html[grid_pos-100:grid_pos+1000])


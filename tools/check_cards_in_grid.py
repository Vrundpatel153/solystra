with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
pos_grid = html.find('id="products-catalog-grid"')
grid_content = html[pos_grid:pos_grid+3000]
print("Grid start snippet:")
print(grid_content[:500])

# Count children inside grid
cards = re.findall(r'<div[^>]*class="[^"]*group[^"]*"', html)
print("Divs with class group:", len(cards))


with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_grid = html.find('id="products-catalog-grid"')
# Let's search backwards for '<div class="max-w' or '<section'
idx = html.rfind('max-w', 0, pos_grid)
print("Last max-w before grid is at:", idx)
if idx != -1:
    print(html[idx-50:idx+400])


with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_grid = html.find('id="products-catalog-grid"')
# Let's see 1000 characters before pos_grid
print(html[pos_grid-1200:pos_grid+100])


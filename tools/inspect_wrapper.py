with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="products-catalog-grid"')
# Let's print 2000 chars before pos
print(html[max(0, pos-2000):pos])


with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="products-catalog-grid"')
if pos != -1:
    print("Around products-catalog-grid:\n", html[pos-500:pos+300])

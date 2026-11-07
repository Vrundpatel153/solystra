with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('id="pdp-main-img"')
pos_right = html.find('lg:col-span-5')
print("Updated left column:\n", html[pos-100:pos_right])


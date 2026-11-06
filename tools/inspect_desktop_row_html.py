with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_desk = html.find('hidden lg:flex items-center justify-between')
print(html[pos_desk:pos_desk+2500])


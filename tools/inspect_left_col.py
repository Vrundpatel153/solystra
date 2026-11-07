with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_start = html.find('lg:col-span-7')
pos_right = html.find('lg:col-span-5')

print("Left column length:", pos_right - pos_start)
print(html[pos_start:pos_right])


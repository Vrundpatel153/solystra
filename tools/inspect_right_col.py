with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_right = html.find('lg:col-span-5')
pos_tabs = html.find('SPECIFICATIONS & PURITY')

print("Right column structure snippet:\n")
print(html[pos_right:pos_right+3500])


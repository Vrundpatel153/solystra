with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function initProductsPage()')
pos_end = text.find('function initCheckoutPage()', pos)
print("initProductsPage snippet length:", pos_end - pos)
print(text[pos:pos+4000])


with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos_start = js.find('window.initProductsPage = initProductsPage;')
if pos_start == -1:
    pos_start = js.find('function initProductsPage()')

pos_end = js.find('// Checkout Page initialization', pos_start)

print("initProductsPage found from index", pos_start, "to", pos_end)
print("First 200 chars:")
print(js[pos_start:pos_start+200])
print("Last 200 chars:")
print(js[pos_end-200:pos_end])


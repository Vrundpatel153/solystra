with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

idx1 = c.find('function initProductsPage')
idx2 = c.find('function initCheckoutPage')
if idx1 != -1:
    print(c[idx1:idx1+1500])


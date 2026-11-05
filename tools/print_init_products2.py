import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

idx1 = c.find('function initProductsPage')
if idx1 != -1:
    print(c[idx1+1400:idx1+3500])

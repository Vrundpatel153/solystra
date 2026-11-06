with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('7-Day Exchanges')
s = text.rfind('<div class="grid grid-cols-4', 0, idx)
e = text.find('</div>', text.find('1-Year Warranty', idx)) + len('</div>')
e = text.find('</div>', e) + len('</div>')
print('=== CURRENT PDP TRUST BADGES ===')
print(text[s:e])

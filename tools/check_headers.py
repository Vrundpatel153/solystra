with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<h1[^>]*>.*?</h1>', text)
print('H1 in products.html:', matches)

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    text2 = f.read()
matches2 = re.findall(r'<h1[^>]*>.*?</h1>', text2)
print('H1 in categories.html:', matches2)

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<script[^>]*src=.*app\.js', text)]
for m in matches:
    print(text[m:m+120])

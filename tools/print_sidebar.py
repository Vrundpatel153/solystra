with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
pos = html.find('aside')
if pos != -1:
    end_aside = html.find('</aside>', pos)
    print("=== ASIDE (DESKTOP SIDEBAR) ===")
    print(html[pos:end_aside+8])
else:
    print("No aside found")


with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

pos = c.find('banner_pc_2.webp', 2000)
print("Second pos:", pos)
print(c[pos-200:pos+3000])

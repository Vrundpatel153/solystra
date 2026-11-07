with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Find hero section
pos = c.find('data-hero-slide="0"')
end = c.find('</section>', pos)
print(c[pos-200:end])

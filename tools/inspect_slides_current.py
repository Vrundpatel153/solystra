with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

for m in re.finditer(r'data-hero-slide="(\d+)"', html):
    slide_num = m.group(1)
    pos = m.start()
    start = html.rfind('<div', 0, pos)
    end = html.find('>', pos)
    print(f'Slide {slide_num}:', html[start:end+1])

# Also check hero dots
for m in re.finditer(r'id="hero-dot-(\d+)"', html):
    dot_num = m.group(1)
    pos = m.start()
    start = html.rfind('<button', 0, pos)
    end = html.find('>', pos)
    print(f'Dot {dot_num}:', html[start:end+1])

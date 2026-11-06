with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find hero-dot
for m in re.finditer(r'id=["\']hero-dot-\d+["\']', html):
    pos = m.start()
    print("DOT:", html[pos-40:pos+120])

# Find all 4 hero slides
for i in range(4):
    m = re.search(rf'id=["\']hero-slide-{i}["\']', html)
    if m:
        pos = m.start()
        # Find the opening tag
        start_tag = html.rfind('<div', 0, pos)
        end_tag = html.find('>', pos)
        print(f"\nSLIDE {i} TAG:\n", html[start_tag:end_tag+1])
        # Find picture / img inside slide i
        next_slide = html.find(f'id="hero-slide-{i+1}"', pos) if i < 3 else html.find('hero-dot', pos)
        slide_chunk = html[start_tag:next_slide]
        img_match = re.search(r'<img[^>]*>', slide_chunk)
        if img_match:
            print(f"SLIDE {i} IMG:", img_match.group(0))


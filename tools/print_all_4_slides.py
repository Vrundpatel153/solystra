with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

import re
for i in range(4):
    slide_id = f'id="hero-slide-{i}"'
    idx = text.find(slide_id)
    if idx != -1:
        print(f"\n=================== SLIDE {i} ===================")
        print(text[idx:idx+1200])


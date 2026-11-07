with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for slide_id in ["hero-slide-2", "hero-slide-3"]:
    pos = text.find(f'id="{slide_id}"')
    if pos != -1:
        end_pos = text.find('id="hero-slide-', pos + 1)
        if end_pos == -1:
            end_pos = text.find('id="hero-dot-0"', pos)
        print(f"=== {slide_id} ===")
        print(text[pos:end_pos])


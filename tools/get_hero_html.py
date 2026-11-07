with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
start_idx = text.find('id="hero-slide-0"')
end_idx = text.find('<!-- Slider Dots -->')
if start_idx != -1 and end_idx != -1:
    # Go back to find opening <div of hero-slide-0
    div_start = text.rfind('<div', 0, start_idx)
    hero_block = text[div_start:end_idx]
    print(hero_block)
else:
    print('Could not find hero block!')

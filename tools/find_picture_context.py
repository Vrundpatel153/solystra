with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

pos = 0
for i in range(4):
    p = text.find('<picture>', pos)
    if p == -1:
        break
    p_end = text.find('</picture>', p)
    print(f"Picture {i+1} at index {p}:")
    print(text[p:p_end+10])
    # Also find surrounding context up to next </picture> or closing tags
    wrapper_start = text.rfind('<div', 0, p)
    slide_start = text.rfind('swiper-slide', 0, p)
    print("Slide class context:", text[slide_start-20:slide_start+40])
    pos = p_end + 10


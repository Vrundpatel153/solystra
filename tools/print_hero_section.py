with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find hero swiper container
m = re.search(r'<!--\s*Hero Swiper Slider\s*-->.*?</section>', text, re.DOTALL)
if m:
    print(m.group(0))
else:
    # try finding swiper-wrapper
    m2 = re.search(r'<div class=\"swiper-wrapper\">.*?</div>\s*<!--\s*Pagination', text, re.DOTALL)
    if m2:
        print(m2.group(0))
    else:
        print("Hero section not found by regex")


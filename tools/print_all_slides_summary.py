with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find all swiper-slide in hero
slides = re.findall(r'<div class="swiper-slide[^"]*".*?</div>(?=\s*<div class="swiper-slide|\s*</div>\s*<div class="absolute bottom-4)', text, re.DOTALL)
print(f"Total slides found: {len(slides)}")
for idx, s in enumerate(slides):
    print(f"\n==================== SLIDE {idx+1} ====================")
    # print picture tag
    pic = re.search(r'<picture>.*?</picture>', s, re.DOTALL)
    if pic:
        print("PICTURE:")
        print(pic.group(0))
    # print title
    title = re.search(r'<h2[^>]*>(.*?)</h2>', s, re.DOTALL)
    if title:
        print("TITLE:", title.group(1))
    sub = re.search(r'<p[^>]*>(.*?)</p>', s, re.DOTALL)
    if sub:
        print("DESC:", sub.group(1))


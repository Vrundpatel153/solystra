with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div[^>]*class=\"[^\"]*hero-slide[^\"]*\"[\s\S]*?</div>\s*</div>\s*</div>', text)
print(f"Found {len(matches)} hero slides")
for i, m in enumerate(matches):
    print(f"\n--- Slide {i+1} ---")
    # find picture or img tags
    pics = re.findall(r'<picture[\s\S]*?</picture>', m)
    if pics:
        for p in pics:
            print("  Picture:", p.strip())
    else:
        imgs = re.findall(r'<img[^>]+>', m)
        for im in imgs:
            print("  Img:", im.strip())
    # find heading
    h = re.findall(r'<h[123][^>]*>[\s\S]*?</h[123]>', m)
    for heading in h:
        print("  Heading:", heading.strip())


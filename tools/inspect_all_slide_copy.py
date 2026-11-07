with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

slides = re.findall(r'<div[^>]*data-hero-slide="(\d+)"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</div>', c, re.DOTALL)
print(f"Found {len(slides)} hero slides:")
for num, s_body in slides:
    h2 = re.search(r'<h2[^>]*>([^<]+)</h2>', s_body)
    sub = re.search(r'<p[^>]*>([^<]+)</p>', s_body)
    pic = re.search(r'<picture>(.*?)</picture>', s_body, re.DOTALL)
    print(f"Slide {num}: H2={h2.group(1) if h2 else 'none'}")
    print(f"  Sub={sub.group(1) if sub else 'none'}")
    if pic:
        srcs = re.findall(r'(?:srcset|src)="([^"]+)"', pic.group(1))
        print(f"  Images: {srcs}")


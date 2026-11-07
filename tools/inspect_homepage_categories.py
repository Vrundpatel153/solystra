with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

pos = c.find('Explore by Category')
end_pos = c.find('</section>', pos)
sub = c[pos:end_pos]

imgs = re.findall(r'<img[^>]+>', sub)
print(f"Total img tags in Category section: {len(imgs)}")
for img in imgs:
    alt = re.search(r'alt="([^"]*)"', img)
    src = re.search(r'src="([^"]*)"', img)
    print("Img:", alt.group(1) if alt else 'none', "->", src.group(1) if src else 'none')

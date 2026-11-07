with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

pos = c.find('hero-banner')
if pos == -1:
    pos = c.find('hero')
print("Hero search pos:", pos)

# Find all banner image references
banners = re.findall(r'<img[^>]+banner[^>]+>', c, re.IGNORECASE)
print(f"Found {len(banners)} banner img tags:")
for b in banners:
    print(" -", b)

# Also check for picture tags or banner classes
pictures = re.findall(r'<picture[^>]*>.*?</picture>', c, re.DOTALL)
print(f"Found {len(pictures)} picture tags:")
for p in pictures:
    print(" -", p[:200])

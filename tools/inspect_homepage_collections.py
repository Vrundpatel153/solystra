with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

pos = c.find('Curated Collections')
if pos == -1:
    pos = c.find('CURATED')
end_pos = c.find('</section>', pos)
sub = c[pos:end_pos]

imgs = re.findall(r'<img[^>]+>', sub)
print(f"Total img tags in Collections section: {len(imgs)}")
for img in imgs:
    alt = re.search(r'alt="([^"]*)"', img)
    src = re.search(r'src="([^"]*)"', img)
    print("Img:", alt.group(1) if alt else 'none', "->", src.group(1) if src else 'none')

# Check also in app.js for collection data
with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    js_c = f.read()

col_idx = js_c.find('COLLECTIONS =')
if col_idx == -1:
    col_idx = js_c.find('collections =')
if col_idx != -1:
    print("\nFound collections in app.js:")
    print(js_c[col_idx:col_idx+1200])


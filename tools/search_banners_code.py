with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

import re
print("Searching for banner-1 in index.html:")
for m in re.finditer(r'banner[^\s\"\']+', text):
    print(m.group(0))

print("\nSearching for collections carousel in index.html:")
for m in re.finditer(r'collection[^\s\"\']+', text):
    print(m.group(0))

print("\nSearching in app.js:")
with open('jewellery-design-html/js/app.js', encoding='utf-8') as f:
    app_text = f.read()

for m in re.finditer(r'banner[^\s\"\']+', app_text):
    print('app.js:', m.group(0))
    break

# Find HERO_SLIDES or similar in app.js:
for m in re.finditer(r'const\s+[A-Z_]*SLIDES|const\s+[A-Z_]*BANNERS|const\s+[A-Z_]*COLLECTIONS', app_text):
    print('Found const in app.js:', m.group(0))


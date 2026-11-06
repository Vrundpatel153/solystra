with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Categories in index.html:")
for m in re.finditer(r'src="solystra_assets/categories/zavya_style/([^"]+)"', text):
    print(" ", m.group(0))

print("\nCollections in index.html:")
for m in re.finditer(r'src="solystra_assets/collections/([^"]+)"', text):
    print(" ", m.group(0))


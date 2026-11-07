with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# search for activeHotspotItemId or auto-activate
for m in re.finditer(r'setActiveHotspot\(.*?\)', text):
    print(m.group(0))

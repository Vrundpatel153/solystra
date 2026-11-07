with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

import re
indices = [m.start() for m in re.finditer('banner_mob_1.webp', text)]
print("Found banner_mob_1.webp at indices:", indices)
for idx in indices:
    print("--- SNIPPET ---")
    print(text[idx-200:idx+800])


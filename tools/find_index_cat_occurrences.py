with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
for m in re.finditer(r'solystra_assets/(?:categories|collections)/[a-zA-Z0-9_\-\./]+', c):
    start = max(0, m.start() - 200)
    end = min(len(c), m.end() + 200)
    print("Match:", m.group(0))
    print(c[start:end].replace('\n', ' '))
    print('='*50)


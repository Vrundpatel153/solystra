with open('jewellery-design-html/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.via-[^{]*\{[^}]*\})', css)
for m in matches[:10]:
    print(m)
print('Total via rules:', len(matches))

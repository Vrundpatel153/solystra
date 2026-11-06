with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'aspect-\[16/11\]', text):
    start = max(0, m.start() - 200)
    end = min(len(text), m.end() + 200)
    print(text[start:end])
    print('---')


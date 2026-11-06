with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'7-Day Exchanges', text):
    start = max(0, m.start() - 300)
    end = min(len(text), m.end() + 300)
    print("Match at index", m.start())
    print(text[start:end])
    print("="*60)

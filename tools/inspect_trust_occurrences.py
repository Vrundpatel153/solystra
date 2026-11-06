with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'7-Day Exchanges', text)]
for idx in matches:
    print(f"Index: {idx}")
    print(text[max(0, idx-100):min(len(text), idx+100)])
    print("-" * 50)


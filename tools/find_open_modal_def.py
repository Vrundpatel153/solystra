import re

with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

matches = [m.start() for m in re.finditer(r'openMobileFilterModal', text)]
for idx, pos in enumerate(matches):
    print(f"Match {idx+1} at {pos}:")
    print(text[max(0, pos-100):min(len(text), pos+300)])
    print("="*60)


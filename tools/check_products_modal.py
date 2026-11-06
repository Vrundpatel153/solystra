with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

matches = list(re.finditer(r'id=["\'](?:mobile-)?filter-modal["\']', html))
print(f"Found {len(matches)} matches in products.html:")
for m in matches:
    pos = m.start()
    print("--- Match at", pos, "---")
    print(html[max(0, pos-200):pos+400])

# Also check for any filter modal or drawer in products.html
print("\nAny filter buttons in products.html:")
for m in re.finditer(r'openFilterModal|openMobileFilterModal', html):
    pos = m.start()
    print("Call at", pos, ":", html[max(0, pos-100):pos+150])

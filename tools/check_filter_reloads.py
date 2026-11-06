with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'window\.location[^\'"]*[\'"][^\'"]*[\'"]', text)
print("Found location reloads:")
for m in set(matches):
    print(" - ", m)

# Also check for onclick attributes in sidebar / filter buttons
sidebar_matches = re.findall(r'<button[^>]+filter[^>]*>', text, re.IGNORECASE)
print(f"Found {len(sidebar_matches)} filter button tags in products.html")
for sm in sidebar_matches[:10]:
    print("  ", sm[:100])

import re

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<section class="bg-white border-b[\s\S]*?</section>', html)
if m:
    print("Found top pills section:")
    print(m.group(0)[:1200])
else:
    print("No section.bg-white.border-b found, searching for other pill containers...")
    matches = re.findall(r'<button[^>]*onclick="[^"]*category[^"]*"[^>]*>[\s\S]*?</button>', html)
    print(f"Found {len(matches)} category onclick buttons in products.html")
    for btn in matches[:10]:
        print("  ", btn[:150])


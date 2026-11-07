with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<section[^>]*id=\"([^\"]+)\"', text)
print("Sections in index.html:", matches)

# Find img tags inside first 3 sections
for m in re.finditer(r'<img[^>]+src=\"([^\"]+)\"[^>]*>', text[:15000]):
    print("img src:", m.group(1))

# Find picture tags
for m in re.finditer(r'<picture[\s\S]*?</picture>', text[:15000]):
    print("picture tag:", m.group(0)[:200])


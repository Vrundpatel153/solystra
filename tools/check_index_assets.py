import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = set(re.findall(r'solystra_assets/(?:categories|collections)/[^\s"\'?]+', text))
for m in sorted(matches):
    print(m)

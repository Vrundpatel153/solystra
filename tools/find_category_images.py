import re

for page in ['jewellery-design-html/categories.html', 'jewellery-design-html/index.html']:
    with open(page, 'r', encoding='utf-8') as f:
        c = f.read()
    imgs = set(re.findall(r'src="([^"]*(?:categories|collections|zavya)[^"]*)"', c))
    print(f"=== {page} ===")
    for img in sorted(imgs):
        print(" ", img)


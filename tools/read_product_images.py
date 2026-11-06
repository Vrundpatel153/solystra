with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<img' in l or 'aspect-' in l:
        print(f"L{i+1}: {l.strip()[:140]}")


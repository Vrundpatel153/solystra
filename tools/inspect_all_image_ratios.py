import re

def inspect_file(file_path):
    print(f"\n======================================")
    print(f"FILE: {file_path}")
    print(f"======================================")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Search for all aspect-* classes
    aspects = re.findall(r'aspect-[a-zA-Z0-9\-\/\[\]]+', content)
    print("Distinct aspect ratios found in file:")
    for a in sorted(set(aspects)):
        print(f"  - {a}")
        
    # 2. Find elements containing aspect-* and print context
    print("\nContainers using aspect ratios:")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'aspect-' in line:
            # find surrounding tag
            start = max(0, i - 1)
            end = min(len(lines), i + 2)
            snippet = " ".join([l.strip() for l in lines[start:end]])
            print(f"  Line {i+1}: {snippet[:140]}...")

inspect_file('jewellery-design-html/product.html')
inspect_file('jewellery-design-html/products.html')
inspect_file('jewellery-design-html/index.html')
inspect_file('jewellery-design-html/js/app.js')


import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

target_str = 'class="lg:col-span-7 lg:sticky lg:top-20 self-start flex flex-col-reverse sm:flex-row gap-4"'
replacement_str = 'class="lg:col-span-7 flex flex-col-reverse sm:flex-row gap-4"'

files_to_update = [
    'jewellery-design-html/product.html',
    'jewellery-design-html-dist/product.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\product.html'
]

for file_path in files_to_update:
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if target_str in content:
        content = content.replace(target_str, replacement_str)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated HTML:", file_path)
    else:
        print("Target string not found in:", file_path)

# Update React ProductDetailPage.jsx
react_path = 'src/pages/ProductDetailPage.jsx'
if os.path.exists(react_path):
    with open(react_path, 'r', encoding='utf-8') as f:
        r_content = f.read()
    r_target = 'className="lg:col-span-7 lg:sticky lg:top-20 self-start flex flex-col-reverse sm:flex-row gap-4"'
    r_repl = 'className="lg:col-span-7 flex flex-col-reverse sm:flex-row gap-4"'
    if r_target in r_content:
        r_content = r_content.replace(r_target, r_repl)
        with open(react_path, 'w', encoding='utf-8') as f:
            f.write(r_content)
        print("Updated React:", react_path)
    else:
        print("React target not found")

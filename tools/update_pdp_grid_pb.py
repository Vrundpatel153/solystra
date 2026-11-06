import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update product.html in all 3 targets
target_grid = 'class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start"'
repl_grid = 'class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start lg:pb-24"'

for p in [
    'jewellery-design-html/product.html',
    'jewellery-design-html-dist/product.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\product.html'
]:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if target_grid in c:
        c = c.replace(target_grid, repl_grid)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated grid pb in {p}")
    else:
        print(f"Target grid not found in {p}")

# 2. Update React ProductDetailPage.jsx
react_p = 'src/pages/ProductDetailPage.jsx'
with open(react_p, 'r', encoding='utf-8') as f:
    rc = f.read()
r_target = 'className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start"'
r_repl = 'className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start lg:pb-24"'
if r_target in rc:
    rc = rc.replace(r_target, r_repl)
    with open(react_p, 'w', encoding='utf-8') as f:
        f.write(rc)
    print("Updated React ProductDetailPage.jsx")
else:
    print("React grid target not found")


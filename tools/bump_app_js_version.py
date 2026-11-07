import os

prod_html_path = os.path.abspath('jewellery-design-html/product.html')

with open(prod_html_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = 'src="js/app.js?v=small_modal_v14"'
replacement = 'src="js/app.js?v=pdp_modal_v1"'

if target in c:
    c = c.replace(target, replacement)
    with open(prod_html_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Bumped app.js version to v=pdp_modal_v1 in product.html!")
else:
    print("Version string not matched!")

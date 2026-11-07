with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Find the exact block under pdp-main-img
pos_img = html.find('id="pdp-main-img"')
pos_right_col = html.find('lg:col-span-5')

left_block = html[pos_img:pos_right_col]
print("Inside left column after pdp-main-img:\n")
print(left_block)

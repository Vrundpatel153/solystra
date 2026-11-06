with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos_init = text.find('function initProductsPage()')
pos_end = text.find('function initCheckoutPage()', pos_init)

print("initProductsPage span:", pos_init, "to", pos_end, "(bytes:", pos_end - pos_init, ")")
# Let's see all sub-functions and event listeners in initProductsPage
import re
print("Functions declared inside initProductsPage:")
for m in re.finditer(r'(function\s+([a-zA-Z0-9_]+)|window\.([a-zA-Z0-9_]+)\s*=)', text[pos_init:pos_end]):
    print(" -", m.group(0))


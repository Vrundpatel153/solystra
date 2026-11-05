import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Available offers')
if idx != -1:
    parent_start = text.rfind('<div class="space-y-2', 0, idx)
    parent_end = text.find('</button></div></div>', idx) + len('</button></div></div>')
    print("PARENT START:", parent_start)
    print("PARENT END:", parent_end)
    print("CONTENT:")
    print(text[parent_start:parent_end])


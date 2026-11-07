import os

prod_html_path = os.path.abspath('jewellery-design-html/product.html')

with open(prod_html_path, 'r', encoding='utf-8') as f:
    c = f.read()

target = '<button aria-label="Enlarge Image" class="p-2.5 rounded-full bg-white/90 hover:bg-[#61532E] text-stone-700 hover:text-white transition-all shadow-xs border border-stone-200 cursor-pointer">'
replacement = '<button aria-label="Enlarge Image" onclick="window.openImageLightbox && window.openImageLightbox()" class="p-2.5 rounded-full bg-white/90 hover:bg-[#61532E] text-stone-700 hover:text-white transition-all shadow-xs border border-stone-200 cursor-pointer">'

if target in c:
    c = c.replace(target, replacement)
    with open(prod_html_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Successfully added inline onclick to Enlarge Image button in product.html!")
else:
    print("Target not found or already updated!")


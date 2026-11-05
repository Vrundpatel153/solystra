import re

def update_html_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Find the banner section
    pattern = r'<section class="relative overflow-hidden bg-stone-900 border-b border-\[#CEBDA7\]"><div class="relative w-full h-36 xs:h-40 sm:h-48 md:h-56"><img alt="([^"]+)" class="w-full h-full object-cover object-center" src="([^"]+)"/><div class="absolute inset-0 bg-gradient-to-r from-black/[^"]+"></div>'
    
    def repl(m):
        alt = m.group(1)
        return (
            '<section class="relative overflow-hidden bg-[#1F190E] border-b border-[#CEBDA7]">'
            '<div class="relative w-full h-44 xs:h-48 sm:h-56 md:h-64 lg:h-72">'
            '<picture class="block w-full h-full">'
            '<source media="(min-width: 640px)" srcset="solystra_assets/banners/catalog_luxury_banner_pc.webp?v=atelier2026">'
            f'<img alt="{alt}" class="w-full h-full object-cover object-right sm:object-center transition-transform duration-700 hover:scale-101" src="solystra_assets/banners/catalog_luxury_banner_mobile.webp?v=atelier2026" loading="eager"/>'
            '</picture>'
            '<div class="absolute inset-0 bg-gradient-to-r from-[#141007]/90 via-[#201A0E]/65 to-black/20"></div>'
        )

    new_c, count = re.subn(pattern, repl, c)
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f"Updated {path} ({count} matches)")
    else:
        print(f"No match in {path}")

html_files = [
    'jewellery-design-html/products.html',
    'jewellery-design-html-dist/products.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\products.html',
    'jewellery-design-html/categories.html',
    'jewellery-design-html-dist/categories.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\categories.html',
    'jewellery-design-html/offers.html',
    'jewellery-design-html-dist/offers.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\offers.html'
]

for p in html_files:
    update_html_file(p)


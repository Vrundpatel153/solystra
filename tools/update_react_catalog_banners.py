import re

def update_jsx(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    pattern = r'<section className="relative overflow-hidden bg-stone-900 border-b border-\[#CEBDA7\]">.*?<div className="relative w-full h-36 xs:h-40 sm:h-48 md:h-56">.*?<img\s+src="[^"]+"\s+alt="([^"]+)"[^>]*/>.*?{/\* Luxury Editorial Scrim \*/}\s*<div className="absolute inset-0 bg-gradient-to-r from-black/[^>]+/>'

    replacement = (
        '<section className="relative overflow-hidden bg-[#1F190E] border-b border-[#CEBDA7]">\n'
        '        <div className="relative w-full h-44 xs:h-48 sm:h-56 md:h-64 lg:h-72">\n'
        '          <picture className="block w-full h-full">\n'
        '            <source media="(min-width: 640px)" srcSet="solystra_assets/banners/catalog_luxury_banner_pc.webp?v=atelier2026" />\n'
        '            <img\n'
        '              src="solystra_assets/banners/catalog_luxury_banner_mobile.webp?v=atelier2026"\n'
        '              alt="\\1"\n'
        '              className="w-full h-full object-cover object-right sm:object-center transition-transform duration-700 hover:scale-101"\n'
        '              loading="eager"\n'
        '            />\n'
        '          </picture>\n\n'
        '          {/* Luxury Editorial Scrim */}\n'
        '          <div className="absolute inset-0 bg-gradient-to-r from-[#141007]/90 via-[#201A0E]/65 to-black/20" />'
    )

    new_c, count = re.subn(pattern, replacement, c, flags=re.DOTALL)
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f"Updated {path} ({count} matches)")
    else:
        print(f"No match in {path}")

for p in ['src/pages/AllProductsPage.jsx', 'src/pages/CategoriesPage.jsx', 'src/pages/OffersPage.jsx']:
    update_jsx(p)


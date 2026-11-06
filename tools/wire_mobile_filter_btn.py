import sys

sys.stdout.reconfigure(encoding='utf-8')

target_btn = '<button class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl border border-[#CEBDA7] bg-[#FAF8F5] hover:bg-[#F5F0EA] active:scale-[0.98] text-xs font-semibold text-stone-800 shadow-2xs transition-all cursor-pointer">'
replacement_btn = '<button onclick="window.openMobileFilterModal()" class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl border border-[#CEBDA7] bg-[#FAF8F5] hover:bg-[#F5F0EA] active:scale-[0.98] text-xs font-semibold text-stone-800 shadow-2xs transition-all cursor-pointer">'

for path in ['jewellery-design-html/products.html', 'jewellery-design-html/categories.html', 'jewellery-design-html/offers.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if target_btn in content:
            content = content.replace(target_btn, replacement_btn)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {path}")
        else:
            print(f"Target not found in {path}")
    except Exception as e:
        print(f"Error {path}: {e}")


import re

with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    c = f.read()

start = c.find('<section class="relative w-full overflow-hidden bg-stone-900')
end = c.find('</section>', start) + len('</section>')
hero = c[start:end]
opens = len(re.findall(r'<div[\s>]', hero))
closes = len(re.findall(r'</div>', hero))
print(f'Hero section: opens={opens}, closes={closes}')

# Check curated accordion in index.html
print('subcat-menu-mob-curated in index.html:', 'subcat-menu-mob-curated' in c)
print('chevron-mob-curated in index.html:', 'chevron-mob-curated' in c)

# Check products.html
with open('jewellery-design-html/products.html', encoding='utf-8') as f:
    p_html = f.read()
print('subcat-menu-mob-curated in products.html:', 'subcat-menu-mob-curated' in p_html)

# Check app.js
with open('jewellery-design-html/js/app.js', encoding='utf-8') as f:
    js = f.read()
print('setCatalogFilterState in app.js:', 'setCatalogFilterState' in js)
print('applyMobileFiltersAndClose in app.js:', 'applyMobileFiltersAndClose' in js)
print('toggleMobileFilterCategory in app.js:', 'toggleMobileFilterCategory' in js)
print('allKeys curated in app.js:', "'curated'" in js)


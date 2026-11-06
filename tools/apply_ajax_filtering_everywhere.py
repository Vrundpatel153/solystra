import re

print("Applying smooth in-page filter state to app.js and products.html...")

# 1. Update app.js
with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Update openMobileFilterModal in app.js
old_modal_start = "m.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-end sm:items-center justify-center font-sans';"
new_modal_start = "m.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-end sm:items-center justify-center font-sans p-2 sm:p-4 pb-16 sm:pb-4';"

if old_modal_start in app_js:
    app_js = app_js.replace(old_modal_start, new_modal_start)
    print("✓ Updated mobile-filter-modal container positioning to clear Netlify badge")

# Ensure modal dialog has safe bottom margin
old_card = 'class="bg-white w-full max-w-lg rounded-t-3xl sm:rounded-2xl p-6 pb-14 sm:pb-6 space-y-4 max-h-[88vh] overflow-y-auto no-scrollbar shadow-2xl border border-stone-200 animate-slide-up"'
new_card = 'class="bg-white w-full max-w-lg rounded-3xl sm:rounded-2xl p-6 pb-8 sm:pb-6 space-y-4 max-h-[82vh] overflow-y-auto no-scrollbar shadow-2xl border border-stone-200 animate-slide-up mb-2 sm:mb-0"'
if old_card in app_js:
    app_js = app_js.replace(old_card, new_card)
    print("✓ Updated modal card max-height and margin")

with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

# 2. Update products.html: eliminate all hard page reloads
with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    products_html = f.read()

# Replace metal & category window.location.href in products.html
replacements = [
    (r"onclick=\"window\.location\.href='products\.html\?metal=silver&amp;category=rings'\"",
     "onclick=\"window.setCatalogFilterState(['rings'], ['silver'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=silver&amp;category=necklaces'\"",
     "onclick=\"window.setCatalogFilterState(['necklaces'], ['silver'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=silver&amp;category=earrings'\"",
     "onclick=\"window.setCatalogFilterState(['earrings'], ['silver'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=silver&amp;category=bracelets'\"",
     "onclick=\"window.setCatalogFilterState(['bracelets'], ['silver'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=silver&amp;category=complete_sets'\"",
     "onclick=\"window.setCatalogFilterState(['complete_sets'], ['silver'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=silver'\"",
     "onclick=\"window.setCatalogFilterState(['all'], ['silver'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=gold&amp;category=rings'\"",
     "onclick=\"window.setCatalogFilterState(['rings'], ['gold'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=gold&amp;category=necklaces'\"",
     "onclick=\"window.setCatalogFilterState(['necklaces'], ['gold'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=gold&amp;category=earrings'\"",
     "onclick=\"window.setCatalogFilterState(['earrings'], ['gold'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=gold&amp;category=bracelets'\"",
     "onclick=\"window.setCatalogFilterState(['bracelets'], ['gold'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=gold&amp;category=complete_sets'\"",
     "onclick=\"window.setCatalogFilterState(['complete_sets'], ['gold'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=gold'\"",
     "onclick=\"window.setCatalogFilterState(['all'], ['gold'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
    (r"onclick=\"window\.location\.href='products\.html\?metal=rose'\"",
     "onclick=\"window.setCatalogFilterState(['all'], ['rose'], []); if(window.closeCategoryDrawer) window.closeCategoryDrawer();\""),
]

count = 0
for pattern, repl in replacements:
    products_html, n = re.subn(pattern, repl, products_html)
    count += n

print(f"✓ Replaced {count} hard page reloads in products.html with instant in-page filtering")

with open('jewellery-design-html/products.html', 'w', encoding='utf-8') as f:
    f.write(products_html)

print("In-page filtering successfully updated!")


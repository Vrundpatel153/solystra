import os
import re

print("Applying cache-busting and defensive filter updates...")

# 1. Update app.js
app_js_path = 'jewellery-design-html/js/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Make applyMobileCategory and applyMobileMetal safe against any reloads
safe_legacy_handlers = """  window.applyMobileCategory = function (cat) {
    if (window.toggleMobileFilterCategory) {
      window.toggleMobileFilterCategory(cat);
    }
  };

  window.applyMobileMetal = function (metal) {
    if (window.toggleMobileFilterMetal) {
      window.toggleMobileFilterMetal(metal);
    }
  };"""

# Check if legacy handlers exist or need to be added
if "window.applyMobileCategory = function" in js:
    # replace existing
    js = re.sub(
        r'window\.applyMobileCategory\s*=\s*function[\s\S]*?window\.applyMobileMetal\s*=\s*function[\s\S]*?};',
        safe_legacy_handlers,
        js
    )
    print("Replaced legacy applyMobileCategory/applyMobileMetal with safe no-reload wrappers!")
else:
    # append before EOF or near openMobileFilterModal
    pos = js.find("window.openMobileFilterModal")
    if pos != -1:
        js = js[:pos] + safe_legacy_handlers + "\n\n  " + js[pos:]
        print("Inserted safe legacy applyMobileCategory/applyMobileMetal wrappers!")

# Ensure topPills and sideCatButtons sync activeCategories and activeMetals
old_top_pills_block = """        if (text.includes('all')) activeCategory = 'all';
        else if (text.includes('bracelet')) activeCategory = 'bracelets';
        else if (text.includes('necklace')) activeCategory = 'necklaces';
        else if (text.includes('ring')) activeCategory = 'rings';
        else if (text.includes('earring')) activeCategory = 'earrings';
        else if (text.includes('suite') || text.includes('set')) activeCategory = 'complete_sets';
        else if (text.includes('chain')) activeCategory = 'necklaces';
        else if (text.includes('anklet')) activeCategory = 'anklets';
        else if (text.includes('bestseller')) activeCategory = 'bestseller';
        else activeCategory = text;

        highlightCategoryPills();
        applyFilters();"""

new_top_pills_block = """        if (text.includes('all')) activeCategory = 'all';
        else if (text.includes('bracelet')) activeCategory = 'bracelets';
        else if (text.includes('necklace')) activeCategory = 'necklaces';
        else if (text.includes('ring')) activeCategory = 'rings';
        else if (text.includes('earring')) activeCategory = 'earrings';
        else if (text.includes('suite') || text.includes('set')) activeCategory = 'complete_sets';
        else if (text.includes('chain')) activeCategory = 'necklaces';
        else if (text.includes('anklet')) activeCategory = 'anklets';
        else if (text.includes('bestseller')) activeCategory = 'bestseller';
        else activeCategory = text;

        activeCategories = [activeCategory];
        highlightCategoryPills();
        applyFilters();
        try {
          const url = new URL(window.location.href);
          if (activeCategory === 'all') url.searchParams.delete('category');
          else url.searchParams.set('category', activeCategory);
          window.history.replaceState({}, '', url.toString());
        } catch (e) {}"""

if old_top_pills_block in js:
    js = js.replace(old_top_pills_block, new_top_pills_block)
    print("Updated topPills click synchronization in app.js!")

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Bump version string across all HTML files to ?v=multiselect_v10
html_files = [
    'jewellery-design-html/index.html',
    'jewellery-design-html/products.html',
    'jewellery-design-html/categories.html',
    'jewellery-design-html/offers.html',
    'jewellery-design-html/product.html',
    'jewellery-design-html/checkout.html',
    'jewellery-design-html/privacy.html',
    'jewellery-design-html/terms.html'
]

for hf in html_files:
    if os.path.exists(hf):
        with open(hf, 'r', encoding='utf-8') as f:
            h_content = f.read()
        
        # replace any js/app.js(?v=[^"']*)?
        new_h, count = re.subn(r'js/app\.js(\?v=[^"\']*)?', 'js/app.js?v=multiselect_v10', h_content)
        if count > 0:
            with open(hf, 'w', encoding='utf-8') as f:
                f.write(new_h)
            print(f"Bumped app.js version in {hf} ({count} replaced)")

print("All cache-busting and defensive updates completed!")


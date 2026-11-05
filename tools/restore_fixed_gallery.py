import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

css_rule = """
/* Fixed Left Product Gallery on Desktop - Only right side scrolls */
@media (min-width: 1024px) {
  .pdp-fixed-gallery {
    position: -webkit-sticky !important;
    position: sticky !important;
    top: calc(74px + 1.25rem) !important; /* 94px: stays fixed with elegant breathing room below 74px header */
    align-self: flex-start !important;
  }
}
"""

def update_css(path):
    if not os.path.exists(path):
        print("CSS not found:", path)
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '.pdp-fixed-gallery' in content:
        content = re.sub(r'/\* Fixed Left Product Gallery[^*]*\*/\s*@media[^{]+\{\s*\.pdp-fixed-gallery\s*\{[^}]+\}\s*\}', '', content)
    content += '\n' + css_rule.strip() + '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated CSS:", path)

def update_html(path):
    if not os.path.exists(path):
        print("HTML not found:", path)
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update gallery container
    old_gallery = 'class="lg:col-span-7 flex flex-col-reverse sm:flex-row gap-4"'
    new_gallery = 'class="lg:col-span-7 pdp-fixed-gallery lg:sticky lg:top-24 self-start flex flex-col-reverse sm:flex-row gap-4"'
    if old_gallery in content:
        content = content.replace(old_gallery, new_gallery)
        print("Updated gallery class in:", path)
    elif 'pdp-fixed-gallery' in content:
        print("Already has pdp-fixed-gallery:", path)
    else:
        # Check if legacy sticky exists
        legacy = 'class="lg:col-span-7 lg:sticky lg:top-20 self-start flex flex-col-reverse sm:flex-row gap-4"'
        if legacy in content:
            content = content.replace(legacy, new_gallery)
            print("Replaced legacy gallery class in:", path)

    # 2. Add cache-buster to atelier_luxury_banner image src so browser loads the new bronze theme
    content = re.sub(
        r'src="solystra_assets/promos/atelier_luxury_banner\.webp(\?[^"]*)?"',
        r'src="solystra_assets/promos/atelier_luxury_banner.webp?v=bronze2026"',
        content
    )
    content = re.sub(
        r'src="/solystra_assets/promos/atelier_luxury_banner\.webp(\?[^"]*)?"',
        r'src="/solystra_assets/promos/atelier_luxury_banner.webp?v=bronze2026"',
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated HTML:", path)

# Update CSS files
update_css('jewellery-design-html/css/styles.css')
update_css('jewellery-design-html-dist/css/styles.css')
update_css(r'c:\Users\vrund\OneDrive\Desktop\solystra-html\css\styles.css')

# Update HTML files
update_html('jewellery-design-html/product.html')
update_html('jewellery-design-html-dist/product.html')
update_html(r'c:\Users\vrund\OneDrive\Desktop\solystra-html\product.html')

# Update React ProductDetailPage.jsx
react_path = 'src/pages/ProductDetailPage.jsx'
if os.path.exists(react_path):
    with open(react_path, 'r', encoding='utf-8') as f:
        r_content = f.read()
    r_old = 'className="lg:col-span-7 flex flex-col-reverse sm:flex-row gap-4"'
    r_new = 'className="lg:col-span-7 pdp-fixed-gallery lg:sticky lg:top-24 self-start flex flex-col-reverse sm:flex-row gap-4"'
    if r_old in r_content:
        r_content = r_content.replace(r_old, r_new)
        print("Updated React gallery class")
    r_content = re.sub(
        r'src="/solystra_assets/promos/atelier_luxury_banner\.webp(\?[^"]*)?"',
        r'src="/solystra_assets/promos/atelier_luxury_banner.webp?v=bronze2026"',
        r_content
    )
    with open(react_path, 'w', encoding='utf-8') as f:
        f.write(r_content)
    print("Updated React file")

print("All updates completed successfully!")

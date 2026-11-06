import os
import re

for fname in os.listdir('jewellery-design-html'):
    if fname.endswith('.html'):
        with open(os.path.join('jewellery-design-html', fname), 'r', encoding='utf-8') as f:
            content = f.read()
            if 'openMobileFilterModal' in content or 'mobile-filter-modal' in content:
                print(f"Found in {fname}")


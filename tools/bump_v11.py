import glob
import re

for hf in glob.glob('jewellery-design-html/*.html'):
    with open(hf, 'r', encoding='utf-8') as f:
        c = f.read()
    new_c, count = re.subn(r'js/app\.js(\?v=[^"\']*)?', 'js/app.js?v=curated_dropdown_v11', c)
    if count > 0:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f"Bumped: {hf}")


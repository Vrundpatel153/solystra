import glob
import re

for fpath in glob.glob('jewellery-design-html/*.html'):
    with open(fpath, 'r', encoding='utf-8') as f:
        t = f.read()
    
    new_t = re.sub(r'js/app\.js(\?v=[a-zA-Z0-9_\-]+)?', 'js/app.js?v=filter_modal_fixed_v12', t)
    new_t = re.sub(r'css/styles\.css(\?v=[a-zA-Z0-9_\-]+)?', 'css/styles.css?v=filter_modal_fixed_v12', new_t)
    
    if new_t != t:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_t)
        print(f"Updated cache buster in {fpath}")


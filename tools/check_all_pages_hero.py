import glob
import re

for html_file in glob.glob('jewellery-design-html/*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    hero_matches = len(re.findall(r'hero-slide', content))
    cta_matches = len(re.findall(r'Shop|Explore|Discover', content))
    print(f"{html_file}: hero-slide={hero_matches}")


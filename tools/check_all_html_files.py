import glob
from bs4 import BeautifulSoup

for f in sorted(glob.glob('jewellery-design-html/*.html')):
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    has_panel = 'collections-dropdown-panel' in content
    has_archive = 'Explore All Categories Archive' in content
    print(f"{f}: panel={has_panel}, archive={has_archive}")


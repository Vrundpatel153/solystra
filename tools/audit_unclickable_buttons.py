from bs4 import BeautifulSoup
import os
import glob

html_files = glob.glob('jewellery-design-html/*.html')

for hf in html_files:
    with open(hf, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Find all elements with text mentioning 'View All', 'Explore', 'See All', 'Shop All'
    for el in soup.find_all(['div', 'button', 'a', 'span']):
        txt = el.get_text(strip=True).lower()
        if any(w in txt for w in ['view all', 'explore all', 'see all', 'browse all']) and len(txt) < 40:
            # Check if this element or any parent up to 3 levels has onclick or href
            curr = el
            has_action = False
            for _ in range(4):
                if curr is None:
                    break
                if curr.get('onclick') or curr.get('href'):
                    has_action = True
                    break
                curr = curr.parent
            if not has_action:
                print(f"[{os.path.basename(hf)}] Missing action on: {el.name} -> '{el.get_text(strip=True)}'")


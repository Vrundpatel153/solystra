from bs4 import BeautifulSoup
import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("=== IMAGES IN INDEX.HTML ===")
for i, img in enumerate(soup.find_all('img')):
    src = img.get('src', '')
    alt = img.get('alt', '')
    parent = img.parent
    gp = parent.parent if parent else None
    
    aspect = "None"
    for el in [img, parent, gp]:
        if el and el.get('class'):
            cls = ' '.join(el.get('class'))
            m = re.search(r'aspect-[a-zA-Z0-9\-\/\[\]]+', cls)
            if m:
                aspect = m.group(0)
                break
    
    # check if width/height attributes or parent classes
    parent_classes = ' '.join(parent.get('class', [])) if parent else ''
    
    print(f"#{i+1}: {src[:45]} | aspect: {aspect} | parent: {parent_classes[:50]}")


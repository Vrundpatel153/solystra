import re
from bs4 import BeautifulSoup

files = [
    'jewellery-design-html/categories.html',
    'jewellery-design-html/index.html',
    'jewellery-design-html/product.html',
    'jewellery-design-html/products.html'
]

for filename in files:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        imgs = [img.get('src') for img in soup.find_all('img') if img.get('src')]
        bg_imgs = re.findall(r'url\((.*?)\)', html)
        all_assets = imgs + [b.strip('\'"') for b in bg_imgs]
        greenish = [x for x in all_assets if any(k in x.lower() for k in ['green', 'zavya', 'collection', 'cat_'])]
        print(f"=== {filename} ===")
        for g in sorted(set(greenish)):
            print(" ", g)
    except Exception as e:
        print(f"Error reading {filename}: {e}")


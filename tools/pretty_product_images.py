from bs4 import BeautifulSoup

with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
if main:
    for i, img in enumerate(main.find_all('img')):
        parent = img.parent
        p_class = parent.get('class', [])
        print(f"\nImage #{i+1}:")
        print(f"  Src: {img.get('src')}")
        print(f"  Alt: {img.get('alt')}")
        print(f"  Parent Tag: {parent.name}")
        print(f"  Parent Classes: {' '.join(p_class)}")
        print(f"  Img Classes: {' '.join(img.get('class', []))}")


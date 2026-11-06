from bs4 import BeautifulSoup

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

grid = soup.find('div', {'id': 'products-catalog-grid'})
if grid:
    children = [c for c in grid.children if c.name == 'div']
    print("Direct div children inside products-catalog-grid:", len(children))
    cards = [c for c in children if 'group' in c.get('class', [])]
    print("Cards with class 'group':", len(cards))
else:
    print("Grid not found!")


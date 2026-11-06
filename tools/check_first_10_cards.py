from bs4 import BeautifulSoup

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

grid = soup.find('div', {'id': 'products-catalog-grid'})
cards = [c for c in grid.children if c.name == 'div' and 'group' in c.get('class', [])]

for i in range(10):
    c = cards[i]
    title = c.find(['h3', 'h4', 'p']).text if c.find(['h3', 'h4', 'p']) else 'No title'
    img = c.find('img')
    img_src = img.get('src', '') if img else 'No img'
    print(f"Card {i+1}: {title.strip()} -> {img_src}")


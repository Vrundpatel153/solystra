from bs4 import BeautifulSoup

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
footer = soup.find('footer')
print("Footer found:", bool(footer))
main = soup.find('main')
print("Main found:", bool(main))
grid = soup.find('div', {'id': 'products-catalog-grid'})
print("Grid parent:", grid.parent.name, grid.parent.get('class'))
print("Grid grandparent:", grid.parent.parent.name, grid.parent.parent.get('class'))

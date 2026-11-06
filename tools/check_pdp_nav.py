from bs4 import BeautifulSoup

with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

nav = soup.find('nav')
if nav:
    print("Nav in product.html:")
    print(nav.prettify())

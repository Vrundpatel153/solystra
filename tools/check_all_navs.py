from bs4 import BeautifulSoup

with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for nav in soup.find_all('nav'):
    print("Found nav:", nav.get('class'))
    print(nav.prettify()[:400])


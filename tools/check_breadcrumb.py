from bs4 import BeautifulSoup

with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

breadcrumb = soup.find('nav', class_=lambda c: c and 'text-stone-500' in c)
if breadcrumb:
    print(breadcrumb.prettify())


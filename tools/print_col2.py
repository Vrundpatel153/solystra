from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target = soup.find(lambda tag: tag.name == 'button' and 'Explore All Categories Archive' in tag.get_text())
col2 = target.find_parent('div', class_=lambda c: c and 'col-span-3' in c)
if col2:
    print("=== COLUMN 2 ===")
    print(col2.prettify())


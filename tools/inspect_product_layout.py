from bs4 import BeautifulSoup

with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

main = soup.find('main')
if main:
    grid = main.find('div', class_=lambda c: c and 'grid' in c)
    if grid:
        print("Product grid classes:", grid.get('class'))
        children = [c for c in grid.children if c.name]
        print(f"Children count: {len(children)}")
        for i, child in enumerate(children):
            print(f"Child {i+1} ({child.name}): class={child.get('class')}")


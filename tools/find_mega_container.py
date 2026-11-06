from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

target = soup.find(lambda tag: tag.name == 'button' and 'Explore All Categories Archive' in tag.get_text())
if target:
    # go up to the mega menu container
    parent = target.parent
    for _ in range(5):
        if parent:
            print("Parent:", parent.name, parent.get('class'))
            parent = parent.parent
    
    # Let's print the entire mega menu container
    menu = target
    for _ in range(4):
        if menu.parent:
            menu = menu.parent
    print("\n--- MENU HTML ---")
    print(menu.prettify()[:3000])

from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find the collections menu root element
menu_root = soup.find(id='collections-menu')
if not menu_root:
    for div in soup.find_all('div'):
        if 'toggleCollectionsMenu' in str(div.parent) or 'toggleCategoryDropdown' in str(div):
            if 'fixed' in div.get('class', []) or 'absolute' in div.get('class', []):
                menu_root = div
                break

if menu_root:
    print("Found menu_root ID:", menu_root.get('id'), "Class:", menu_root.get('class'))
    # print desktop and mobile parts
    print("Desktop part:")
    lg_grid = menu_root.find('div', class_=lambda c: c and 'lg:grid' in c)
    if lg_grid:
        print("lg_grid found!")
    mob_part = menu_root.find('div', class_=lambda c: c and 'lg:hidden' in c)
    if mob_part:
        print("mob_part found!")
        print(mob_part.prettify()[:2000])
else:
    print("Menu root not found by id, let's search by class")
    # search for element with backdrop-blur
    for div in soup.find_all('div', class_=lambda c: c and 'overflow-hidden' in c and 'top-full' in c):
        print("Found top-full dropdown:", div.get('id'), div.get('class'))
        print(div.prettify()[:1000])

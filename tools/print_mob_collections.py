from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# find the container of toggleCollectionsMenu
for div in soup.find_all('div'):
    if div.find(id='subcat-menu-mob-curated'):
        print("Found mobile collections container:")
        print(div.prettify()[:3000])
        break

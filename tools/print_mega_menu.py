from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

menu = soup.find('div', id='desktop-collections-menu')
if not menu:
    # find dropdown
    menu = soup.find('div', class_=lambda c: c and 'grid-cols-12' in c and 'CURATED COLLECTIONS' in soup.text)

# search for "CURATED COLLECTIONS" in soup
for div in soup.find_all('div'):
    if 'CURATED COLLECTIONS' in div.get_text() and 'JEWELRY CATEGORIES' in div.get_text():
        # find the container
        if 'grid' in ' '.join(div.get('class', [])):
            print("Found mega menu grid:")
            print(div.prettify())
            break


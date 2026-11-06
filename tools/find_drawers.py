from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# search for mobile drawer or menu
for div in soup.find_all(['div', 'nav']):
    div_id = div.get('id', '')
    if any(k in div_id.lower() for k in ['drawer', 'nav', 'menu']):
        print(f"Tag: {div.name}, ID: {div_id}, Class: {' '.join(div.get('class', []))[:60]}")

# also search for hamburger button
buttons = soup.find_all('button')
for b in buttons:
    onclick = b.get('onclick', '')
    if 'menu' in onclick.lower() or 'drawer' in onclick.lower():
        print(f"Button onclick: {onclick}")

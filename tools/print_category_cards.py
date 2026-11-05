from bs4 import BeautifulSoup

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cards = soup.find_all('h3')
for i, h3 in enumerate(cards[:10]):
    card_div = h3.find_parent('div', class_=lambda c: c and 'group' in c)
    if card_div:
        img = card_div.find('img')
        img_src = img['src'] if img else 'no-img'
        print(f"Card {i+1}: '{h3.text.strip()}'")
        print(f"  img: {img_src}")
        print(f"  tag: {card_div.name}, class: {card_div.get('class')}")
        print(f"  onclick: {card_div.get('onclick')}")


from bs4 import BeautifulSoup

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cards = soup.find_all('h3')
for i, h3 in enumerate(cards[:10]):
    card_div = h3.find_parent('div', class_=lambda c: c and 'group' in c)
    print(f"--- CARD {i+1}: {h3.text.strip()} ---")
    print(str(card_div)[:300])


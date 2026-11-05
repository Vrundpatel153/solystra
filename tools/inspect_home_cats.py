from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for sec in soup.find_all('section'):
    h2 = sec.find(['h2', 'h3'])
    if h2 and 'Explore by Category' in h2.text:
        print("Found Explore by Category section!")
        cards = sec.find_all('div', class_=lambda c: c and 'group' in c)
        print(f"Cards count: {len(cards)}")
        for i, card in enumerate(cards):
            img = card.find('img')
            title = card.find(['h3', 'h4', 'p', 'span'])
            onclick = card.get('onclick')
            print(f"  Category card {i+1}: title='{title.text.strip() if title else ''}', img='{img.get('src') if img else ''}', onclick='{onclick}'")


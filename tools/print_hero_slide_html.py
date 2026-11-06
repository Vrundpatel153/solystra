from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

slides = soup.find_all(attrs={'data-hero-slide': True})
for i, s in enumerate(slides):
    print(f"--- Slide {i} ---")
    print(s.prettify()[:500])


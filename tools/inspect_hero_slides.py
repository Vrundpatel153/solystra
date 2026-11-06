from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

slides = soup.find_all(attrs={'data-hero-slide': True})
print(f"Total hero slides in index.html: {len(slides)}")
for i, slide in enumerate(slides):
    sources = [s.get('srcset') for s in slide.find_all('source')]
    img = slide.find('img')
    print(f"Slide {i}:")
    print(f"  mobile srcset: {sources}")
    print(f"  img src: {img.get('src') if img else 'none'}")
    print(f"  img alt: {img.get('alt') if img else 'none'}")


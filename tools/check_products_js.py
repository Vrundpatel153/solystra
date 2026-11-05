with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('URLSearchParams')
if idx != -1:
    print("Found URLSearchParams:")
    print(c[max(0, idx-100):min(len(c), idx+600)])
else:
    print("No URLSearchParams found directly in products.html.")

from bs4 import BeautifulSoup
soup = BeautifulSoup(c, 'html.parser')
for s in soup.find_all('script'):
    src = s.get('src')
    if src:
        print("Script src:", src)


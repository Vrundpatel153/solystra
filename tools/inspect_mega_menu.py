from bs4 import BeautifulSoup
import glob

for html_file in ['jewellery-design-html/index.html', 'jewellery-design-html/products.html', 'jewellery-design-html/product.html']:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"=== {html_file} ===")
    idx = content.find('Explore All Categories Archive')
    if idx != -1:
        print(content[idx-200:idx+400])
    else:
        print("Not found in", html_file)


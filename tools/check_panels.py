from bs4 import BeautifulSoup

for fpath in ['jewellery-design-html/index.html', 'jewellery-design-html/products.html', 'jewellery-design-html/product.html']:
    with open(fpath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    panel = soup.find(id='collections-dropdown-panel')
    if panel:
        cat_btn = panel.find(lambda t: t.name == 'button' and 'Categories Archive' in t.get_text())
        print(fpath, "has panel: True, has Categories Archive btn:", cat_btn is not None)
    else:
        print(fpath, "has panel: False")

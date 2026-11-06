with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_pag = text.find('id="catalog-pagination-container"')
pos_footer = text.find('<footer')

print("Between pagination container and footer:")
print(repr(text[pos_pag+len('id="catalog-pagination-container"'):pos_footer]))


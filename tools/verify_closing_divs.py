with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_desk = text.find('<!-- Desktop Control Row')
pos_mob = text.find('<!-- Mobile Control Stack')
pos_grid = text.find('id="products-catalog-grid"')

print("Between Mobile Control Stack and Grid:")
print(repr(text[pos_mob:pos_grid]))

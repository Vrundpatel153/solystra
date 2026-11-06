with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_ctrl = text.find('Unified Catalog Controls')
print('=== BEFORE CONTROLS ===')
print(text[max(0, pos_ctrl-400):pos_ctrl])

pos_grid = text.find('id="products-catalog-grid"')
print('=== BEFORE GRID ===')
print(text[max(0, pos_grid-400):pos_grid])


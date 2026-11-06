with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_banner = html.find('</section>')
pos_grid = html.find('id="products-catalog-grid"')
print(f"Between section end ({pos_banner}) and grid ({pos_grid}): length is {pos_grid - pos_banner}")
print("Content between them:\n")
content = html[pos_banner:pos_grid]
# Print the first 2500 chars of this content
print(content[:2500])


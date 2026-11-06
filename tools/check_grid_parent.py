from bs4 import BeautifulSoup

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_container = text.find('max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8')
pos_footer = text.find('<footer')

soup_chunk = text[pos_container:pos_footer]
print("Chunk length:", len(soup_chunk))

# Check parent of #products-catalog-grid
soup = BeautifulSoup(text, 'html.parser')
grid = soup.find('div', {'id': 'products-catalog-grid'})
if grid:
    print("Parent of grid:", grid.parent.name, grid.parent.get('class'))
    print("Grandparent of grid:", grid.parent.parent.name if grid.parent.parent else None, grid.parent.parent.get('class') if grid.parent.parent else None)


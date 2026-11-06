with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print("Has aside tag:", bool(re.search(r'<aside', html)))
print("Catalog products count id:", bool(re.search(r'id="catalog-products-count"', html)))
print("Mobile catalog count id:", bool(re.search(r'id="mobile-catalog-products-count"', html)))
print("Filter button with openFilterModal:", bool(re.search(r'window\.openFilterModal', html)))
print("Grid class:", re.search(r'id="products-catalog-grid"[^>]*class="([^"]*)"', html).group(1))
print("Catalog pagination container:", bool(re.search(r'id="catalog-pagination-container"', html)))
print("Pagination buttons list:", bool(re.search(r'id="pagination-pages-list"', html)))
print("Total product cards count in HTML:", len(re.findall(r'data-product-card="true"', html)))


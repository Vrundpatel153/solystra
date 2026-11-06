with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_banner = text.find('catalog_luxury_banner_pc.webp')
pos_aside = text.find('<aside')
print("=== FROM BANNER TO ASIDE ===")
print(text[pos_banner:pos_aside])


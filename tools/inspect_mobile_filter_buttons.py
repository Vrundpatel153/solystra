with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="mobile-filter-curated"')
print(text[pos:pos+2500])


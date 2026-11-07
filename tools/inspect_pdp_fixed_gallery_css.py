with open('jewellery-design-html/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos = css.find('.pdp-fixed-gallery')
print(css[pos-50:pos+350])

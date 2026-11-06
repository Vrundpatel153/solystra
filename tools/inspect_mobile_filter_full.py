with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('window.openMobileFilterModal = function')
print(text[pos:pos+5500])


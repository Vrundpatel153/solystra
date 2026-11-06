with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function initProductsCatalog()')
if pos == -1:
    pos = text.find('initProductsCatalog')
print("Position:", pos)
print(text[pos:pos+4000])


with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('openMobileFilterModal')
print("Position in app.js:", pos)
if pos != -1:
    print(text[pos:pos+1500])


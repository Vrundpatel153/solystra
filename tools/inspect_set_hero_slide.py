with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('window.setHeroSlide =')
if pos == -1:
    pos = text.find('function setHeroSlide')
print("Position of setHeroSlide:", pos)
if pos != -1:
    print(text[pos:pos+1500])

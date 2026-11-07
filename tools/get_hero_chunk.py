with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx3 = text.find('id="hero-slide-3"')
print(text[idx3+1300:idx3+2500])

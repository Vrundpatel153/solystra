with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('initStylingCombos')
print(text[idx:idx+3500])

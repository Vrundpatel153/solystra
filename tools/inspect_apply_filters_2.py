with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('if (curTarget === \'heirloom_suites\'')
print(text[pos:pos+4000])


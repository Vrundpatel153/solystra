with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('banner_pc_1.webp')
if idx != -1:
    print(text[idx-400:idx+2500])
else:
    print("banner_pc_1.webp not found")


with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('collection_links.webp')
if idx != -1:
    print(text[idx-200:idx+1500])
else:
    print("collection_links.webp not found")


with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('js/app.js?v=small_modal_v14', 'js/app.js?v=hotspot_smart_v15')

with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Bumped app.js version in index.html!")

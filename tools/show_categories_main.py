with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('group flex items-center justify-between')
pos3 = c.find('</section>', pos)
print(c[pos3:pos3+3000])

with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('openMobileFilterModal')
print("Position:", pos)
if pos != -1:
    print(text[max(0, pos-200):min(len(text), pos+1500)])


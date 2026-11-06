import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Insured Delivery')
if idx != -1:
    start = max(0, idx - 400)
    end = min(len(text), idx + 2000)
    print("Trust badge section snippet:")
    print(text[start:end])
else:
    print("Insured Delivery not found in index.html")

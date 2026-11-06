with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Line 512 in app.js:")
for l in lines[505:525]:
    print(l, end='')

print("\n\nLine 1125-1150 in app.js:")
for l in lines[1124:1150]:
    print(l, end='')


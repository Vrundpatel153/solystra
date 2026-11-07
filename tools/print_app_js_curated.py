with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = 3400
end = 3600
print("".join(lines[start:end]))

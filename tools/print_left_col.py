with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = 3515
end = 3545
for idx, l in enumerate(lines[start:end], start=start+1):
    print(f"{idx}: {l}", end="")

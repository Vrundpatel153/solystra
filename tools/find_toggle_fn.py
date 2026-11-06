with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'toggleCollectionsMenu' in l or 'function toggleCollectionsMenu' in l:
        print(f"L{i+1}:")
        for j in range(max(0, i-5), min(len(lines), i+35)):
            print(lines[j], end='')
        break

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Explore All Categories Archive' in l:
        print(f"Around line {i+1}:")
        for j in range(max(0, i-6), min(len(lines), i+8)):
            print(f"{j+1}: {lines[j]}", end='')


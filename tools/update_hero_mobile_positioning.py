with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = '<div class="absolute inset-0 z-10 flex items-center">'
replacement = '<div class="absolute inset-0 z-10 flex items-end sm:items-center pb-12 sm:pb-0">'

count = c.count(target)
print(f"Found {count} occurrences of target")

new_c = c.replace(target, replacement)
with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(new_c)

print(f"Updated {count} occurrences in index.html")


with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('window.openMobileFilterModal = function')
end = text.find('// Size Guide Modal', start)

# Print lines where helper functions are defined
section = text[start:end]
for line in section.splitlines():
    if 'window.' in line or 'function' in line:
        print(line[:120])


with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('window.openMobileFilterModal = function')
end = text.find('// Size Guide Modal', start)
print(text[start:end])

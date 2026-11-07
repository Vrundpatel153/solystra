with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('const STYLING_COMBOS = [')
end_idx = text.find('let isComboSectionHovered = false;')

print("Start idx:", start_idx)
print("End idx:", end_idx)
print(text[start_idx:end_idx])


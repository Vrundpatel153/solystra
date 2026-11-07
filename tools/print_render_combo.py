with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('function renderCombo(idx)')
if pos != -1:
    end_pos = text.find('function initCollectionsCarousel', pos)
    print(text[pos:end_pos])

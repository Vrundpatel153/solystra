with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('const STYLING_COMBOS = [')
end = text.find('function initCollectionsCarousel', start)
print(text[start:start+1200])
print("\n...\n")
print(text[end-800:end])

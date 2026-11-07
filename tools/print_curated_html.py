with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="curated-looks-section"')
if pos != -1:
    end_pos = text.find('</section>', pos)
    print(text[pos:end_pos+10])

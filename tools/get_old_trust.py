with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('7-Day Exchanges')
sec_start = text.rfind('<section', 0, idx)
sec_end = text.find('</section>', idx) + len('</section>')

old_section = text[sec_start:sec_end]
print("Old Section length:", len(old_section))
print("Start:", old_section[:100])
print("End:", old_section[-100:])


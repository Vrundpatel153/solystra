with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('7-Day Exchanges')
# find enclosing <section>
sec_start = text.rfind('<section', 0, idx)
sec_end = text.find('</section>', idx) + len('</section>')

print("Trust Badges Section:")
print(text[sec_start:sec_end])

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 0
for i in range(4):
    p = text.find('<picture>', pos)
    p_end = text.find('</picture>', p)
    print(f"=== SLIDE {i+1} ===")
    print("BEFORE:\n", text[max(0, p-300):p])
    print("INSIDE:\n", text[p:p_end+10])
    print("AFTER:\n", text[p_end+10:p_end+500])
    pos = p_end + 10


with open('jewellery-design-html/css/styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 0
while True:
    pos = text.find('combo-hotspot-pin', pos)
    if pos == -1:
        break
    print(f"Found combo-hotspot-pin at {pos}:")
    print(text[max(0, pos-100):min(len(text), pos+200)])
    print("=" * 40)
    pos += 17

with open('jewellery-design-html/css/styles.css', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of styles.css:', len(text))
print('Last 500 chars:')
print(text[-500:])


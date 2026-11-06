import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_hero = text.find('hero-slide-0')
start = text.rfind('<section', 0, pos_hero)
end = text.find('</section>', pos_hero) + len('</section>')

hero_block = text[start:end]
print(f'Length of hero block: {len(hero_block)}')

tags = re.findall(r'<(/?[a-zA-Z0-9]+)', hero_block)
stack = []
unmatched = []
for t in tags:
    if t.startswith('/'):
        closing = t[1:].lower()
        if stack and stack[-1] == closing:
            stack.pop()
        else:
            unmatched.append(f'unmatched close </{closing}>')
    elif t.lower() not in ['img', 'br', 'hr', 'input', 'source', 'meta', 'link']:
        stack.append(t.lower())

print('Remaining open tags in hero section:', stack)
print('Unmatched closes in hero section:', unmatched)

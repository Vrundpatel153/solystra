with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

pos_hero = html.find('id="hero-slide-0"')
start = html.rfind('<section', 0, pos_hero)
pos_dots = html.find('id="hero-dot-3"')
end = html.find('</section>', pos_dots) + 10

print("HERO SECTION MARKUP:\n")
print(html[start:end])


with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_hero = text.find('solystra-hero-wrap')
if pos_hero == -1:
    pos_hero = text.find('id="hero-section"')
if pos_hero == -1:
    pos_hero = text.find('<section')

pos_hero_end = text.find('</section>', pos_hero) + len('</section>')
print("Current index.html hero section (first 1000 chars):")
print(text[pos_hero:pos_hero+1000])
print("\nHero section end snippet (last 300 chars):")
print(text[pos_hero_end-300:pos_hero_end])

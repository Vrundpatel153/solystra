with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_hero_start = text.find('solystra-hero-wrap')
if pos_hero_start != -1:
    # Find the <section that starts this
    pos_sec_start = text.rfind('<section', 0, pos_hero_start)
    pos_sec_end = text.find('</section>', pos_hero_start) + len('</section>')
    print(f"Hero section starts at {pos_sec_start} and ends at {pos_sec_end}")
    print("Start snippet (200 chars):")
    print(text[pos_sec_start:pos_sec_start+200])
    print("End snippet (200 chars):")
    print(text[pos_sec_end-200:pos_sec_end])
    print("What comes immediately after hero section (200 chars):")
    print(text[pos_sec_end:pos_sec_end+200])


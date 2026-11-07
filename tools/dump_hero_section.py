with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find('<section class="relative w-full overflow-hidden bg-stone-900')
idx_end = text.find('</section>', idx_start) + len('</section>')

hero_section = text[idx_start:idx_end]
print("Actual hero section length:", len(hero_section))

with open('tools/hero_section_exact.html', 'w', encoding='utf-8') as out:
    out.write(hero_section)
print("Saved tools/hero_section_exact.html")

with open('scratch_cdd8d62_hero.html', 'r', encoding='utf-8') as f:
    hero_4day = f.read()

# Fix active slide 0 state
hero_4day = hero_4day.replace(
    '<div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="0" id="hero-slide-0">',
    '<div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10 pointer-events-auto" data-hero-slide="0" id="hero-slide-0">'
)
# Fix dot active: dot 0 should be w-7 bg-[#C5A059], dot 2 should be w-2
hero_4day = hero_4day.replace(
    '<button aria-label="Slide 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-0"',
    '<button aria-label="Slide 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs" id="hero-dot-0"'
)
hero_4day = hero_4day.replace(
    '<button aria-label="Slide 3" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs" id="hero-dot-2"',
    '<button aria-label="Slide 3" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-2"'
)

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

pos_hero_start = index_html.find('solystra-hero-wrap')
pos_sec_start = index_html.rfind('<section', 0, pos_hero_start)
pos_sec_end = index_html.find('</section>', pos_hero_start) + len('</section>')

print(f"Replacing hero section from {pos_sec_start} to {pos_sec_end}")
new_index_html = index_html[:pos_sec_start] + hero_4day + index_html[pos_sec_end:]

with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_html)

print("Successfully replaced hero section with 4-day-old banner!")

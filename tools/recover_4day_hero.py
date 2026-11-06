def recover_4day_hero():
    index_path = 'jewellery-design-html/index.html'
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the current hero section in index.html
    # It is right after </header> and ends before the trust badges section
    pos_header_end = html.find('</header>') + len('</header>')
    pos_trust = html.find('<!-- Trust / Value Proposition Strip -->')
    if pos_trust == -1:
        pos_trust = html.find('Insured Delivery')
        pos_trust = html.rfind('<section', 0, pos_trust)

    print("Hero section currently spans from", pos_header_end, "to", pos_trust)
    print("Old hero snippet:\n", html[pos_header_end:pos_header_end+200])

    with open('scratch_cdd8d62_hero.html', 'r', encoding='utf-8') as f:
        hero_4day = f.read()

    # Ensure Slide 0 is active on load
    hero_4day = hero_4day.replace('data-hero-slide="0" id="hero-slide-0"', 'data-hero-slide="0" id="hero-slide-0"')
    # make sure slide 0 has opacity-100 z-10
    # In scratch_cdd8d62_hero.html, slide 0 has:
    # class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none"
    # and dot 2 had w-7. Let's make slide 0 opacity-100 and dot 0 w-7
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

    new_html = html[:pos_header_end] + '\n\n    ' + hero_4day + '\n\n    ' + html[pos_trust:]

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully restored 4-day-old hero banner in index.html!")

if __name__ == '__main__':
    recover_4day_hero()


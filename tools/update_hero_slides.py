with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

slides_data = [
    {
        "id": 0,
        "tag": "NEW ARRIVALS",
        "title": "The 18K Gold Suite",
        "desc": "Layered tennis bracelets and kada cuffs in 18K Italian gold vermeil.",
        "btn": "Shop Gold Suites",
        "mob_img": "solystra_assets/banners/banner_mob_1.webp?v=drive2026",
        "pc_img": "solystra_assets/banners/banner_pc_1.webp?v=drive2026",
        "loading": "eager",
        "fetchpriority": "high",
        "active_classes": "opacity-100 z-10 pointer-events-auto"
    },
    {
        "id": 1,
        "tag": "MOST LOVED",
        "title": "Blush Tones Collection",
        "desc": "Delicate pink enamel blossoms and brilliant solitaires.",
        "btn": "Explore Collection",
        "mob_img": "solystra_assets/banners/banner_mob_2.webp?v=drive2026",
        "pc_img": "solystra_assets/banners/banner_pc_2.webp?v=drive2026",
        "loading": "lazy",
        "fetchpriority": None,
        "active_classes": "opacity-0 z-0 pointer-events-none"
    },
    {
        "id": 2,
        "tag": "SIGNATURE PIECES",
        "title": "Modern Classics",
        "desc": "Certified 925 silver bands, huggies and solitaires.",
        "btn": "Shop Classics",
        "mob_img": "solystra_assets/banners/banner_floral_portrait_mob.webp?v=drive2026",
        "pc_img": "solystra_assets/banners/banner_floral_portrait.webp?v=drive2026",
        "loading": "lazy",
        "fetchpriority": None,
        "active_classes": "opacity-0 z-0 pointer-events-none"
    },
    {
        "id": 3,
        "tag": "GIFTING GUIDE",
        "title": "Signature Gift Sets",
        "desc": "Delivered in bespoke velvet keepsake vault with hallmark certificate.",
        "btn": "Discover Gift Sets",
        "mob_img": "solystra_assets/banners/banner_profile_floral_mob.webp?v=drive2026",
        "pc_img": "solystra_assets/banners/banner_profile_floral.webp?v=drive2026",
        "loading": "lazy",
        "fetchpriority": None,
        "active_classes": "opacity-0 z-0 pointer-events-none"
    }
]

slides_html = []
for s in slides_data:
    fp_attr = ' fetchpriority="high"' if s["fetchpriority"] else ''
    slide_markup = f'''<div class="absolute inset-0 transition-opacity duration-700 ease-in-out {s["active_classes"]}" data-hero-slide="{s["id"]}" id="hero-slide-{s["id"]}"><picture><source media="(max-width: 640px)" srcset="{s["mob_img"]}"/><img alt="{s["title"]}" class="w-full h-full object-cover object-center block" loading="{s["loading"]}"{fp_attr} src="{s["pc_img"]}"/></picture><div class="absolute inset-0 hero-scrim-desktop hidden sm:block pointer-events-none" style="background: linear-gradient(90deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.60) 45%, rgba(0,0,0,0.20) 75%, rgba(0,0,0,0) 100%);"></div><div class="absolute inset-0 hero-scrim-mobile sm:hidden pointer-events-none" style="background: linear-gradient(0deg, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.72) 40%, rgba(0,0,0,0.30) 70%, rgba(0,0,0,0) 100%);"></div><div class="absolute inset-0 z-10 flex items-end pb-16 sm:pb-0 sm:items-center"><div class="max-w-7xl w-full mx-auto px-5 sm:px-10 lg:px-14"><div class="max-w-xl text-left"><span class="inline-block text-[11px] sm:text-xs tracking-widest text-[#F5E6CC] uppercase font-semibold mb-1.5 sm:mb-3 hero-tag-shadow" style="text-shadow: 0 1px 4px rgba(0,0,0,0.95), 0 2px 8px rgba(0,0,0,0.75);">{s["tag"]}</span><h2 class="font-serif text-2xl xs:text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-tight tracking-tight hero-title-shadow max-w-full" style="text-shadow: 0 2px 10px rgba(0,0,0,0.95), 0 4px 20px rgba(0,0,0,0.85), 0 1px 3px rgba(0,0,0,0.9);">{s["title"]}</h2><p class="text-xs sm:text-base lg:text-lg text-stone-200 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light hero-desc-shadow max-w-[290px] xs:max-w-sm sm:max-w-lg line-clamp-2 sm:line-clamp-none" style="text-shadow: 0 1px 6px rgba(0,0,0,0.95), 0 2px 14px rgba(0,0,0,0.85);">{s["desc"]}</p><div class="mt-4 sm:mt-7 flex items-center gap-3 sm:gap-4"><button class="hero-cta-button cursor-pointer" onclick="window.location.href=\'products.html\'" style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 22px; font-size: 13px; font-weight: 500; line-height: 1.2; border-radius: 8px; background-color: #61532E; color: #ffffff; box-shadow: 0 4px 14px rgba(0,0,0,0.45); cursor: pointer; border: 1px solid rgba(255,255,255,0.18);"><span>{s["btn"]}</span><svg class="lucide lucide-arrow-right w-4 h-4 text-white/90" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></button><button class="hidden sm:inline-flex items-center text-xs font-medium tracking-wide text-white/90 hover:text-white underline underline-offset-4 decoration-[#C5A059] py-3 px-2 transition-colors cursor-pointer" onclick="window.location.href=\'products.html\'" style="text-shadow: 0 1px 4px rgba(0,0,0,0.85);">Explore All Pieces</button></div></div></div></div></div>'''
    slides_html.append(slide_markup)

new_slides_content = "".join(slides_html)

# Now replace the region in index.html from start of slide 0 to end of slide 3
start_needle = '<div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10 pointer-events-auto" data-hero-slide="0" id="hero-slide-0">'
end_needle = '<div class="absolute bottom-4 inset-x-0 z-20 flex justify-center gap-2">'

idx_start = text.find(start_needle)
idx_end = text.find(end_needle, idx_start)

if idx_start == -1 or idx_end == -1:
    print(f"Error: could not locate needles! idx_start={idx_start}, idx_end={idx_end}")
else:
    old_part = text[idx_start:idx_end]
    new_text = text[:idx_start] + new_slides_content + text[idx_end:]
    with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully updated jewellery-design-html/index.html hero slides!")


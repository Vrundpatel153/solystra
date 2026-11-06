import os
import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'(<section class="relative w-full overflow-hidden bg-stone-900[\s\S]*?</section>)', text)
if m:
    hero_markup = m.group(1)
    print("=== HERO SECTION LENGTH ===", len(hero_markup))
    # Print slide 0 and slide 1 markup
    for slide_idx in range(4):
        s_m = re.search(rf'(<div[^>]*id="hero-slide-{slide_idx}"[\s\S]*?</div>\s*</div>\s*</div>\s*</div>)', hero_markup)
        if s_m:
            print(f"\n--- SLIDE {slide_idx} ---")
            print(s_m.group(1)[:400])
else:
    print("Hero section not found")


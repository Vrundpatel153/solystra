import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Get the pristine index.html from commit 61d23a5
res = subprocess.run(['git', 'show', '61d23a5:jewellery-design-html/index.html'], capture_output=True, text=True, encoding='utf-8')
pristine_html = res.stdout

# Now let's simply replace the banner image paths in pristine_html:
# Slide 0
pristine_html = pristine_html.replace(
    'srcset="solystra_assets/banners/banner_mob_2.webp"',
    'srcset="solystra_assets/banners/hero_model_1_mob.webp?v=model2026"'
).replace(
    'src="solystra_assets/banners/banner_pc_2.webp"',
    'src="solystra_assets/banners/hero_model_1_pc.webp?v=model2026"'
)

# Slide 1
pristine_html = pristine_html.replace(
    'srcset="solystra_assets/banners/banner_blush_tones_mob.webp"',
    'srcset="solystra_assets/banners/hero_model_2_mob.webp?v=model2026"'
).replace(
    'src="solystra_assets/banners/banner_blush_tones_pc.webp"',
    'src="solystra_assets/banners/hero_model_2_pc.webp?v=model2026"'
)

# Slide 2
pristine_html = pristine_html.replace(
    'srcset="solystra_assets/banners/banner_mob_3.webp"',
    'srcset="solystra_assets/banners/hero_model_3_mob.webp?v=model2026"'
).replace(
    'src="solystra_assets/banners/banner_pc_3.webp"',
    'src="solystra_assets/banners/hero_model_3_pc.webp?v=model2026"'
)

# Slide 3
pristine_html = pristine_html.replace(
    'srcset="solystra_assets/banners/banner_gift_sets_mob.webp"',
    'srcset="solystra_assets/banners/hero_model_4_mob.webp?v=model2026"'
).replace(
    'src="solystra_assets/banners/banner_gift_sets_pc.webp"',
    'src="solystra_assets/banners/hero_model_4_pc.webp?v=model2026"'
)

# Also update the titles, tags, and subtitles to match the new models
pristine_html = pristine_html.replace(
    '>NEW ARRIVALS</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">The 18K Gold Suite</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Layered tennis bracelets and kada cuffs in 18K Italian gold vermeil.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html\'"><span>Shop Gold Suites</span>',
    '>ATELIER SIGNATURE</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">The Solitaire Heart Suite</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Pure 925 sterling silver with brilliant Austrian solitaire heart pendant.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html?category=necklaces\'"><span>Explore Necklaces</span>'
)

pristine_html = pristine_html.replace(
    '>MOST LOVED</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">Blush Tones Collection</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Delicate pink enamel blossoms and brilliant solitaires.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html\'"><span>Explore Collection</span>',
    '>MOST LOVED</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">Modern Classics Collection</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Double-layered solitaire diamond and natural freshwater pearl necklace.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html?category=complete-sets\'"><span>Shop Complete Sets</span>'
)

pristine_html = pristine_html.replace(
    '>SIGNATURE PIECES</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">Modern Classics</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Certified 925 silver bands, huggies and solitaires.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html\'"><span>Shop Classics</span>',
    '>NEW ARRIVALS</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">Royal Crown Solitaire</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Bespoke tiara-cut dancing solitaire in handcrafted 925 sterling silver.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html?category=necklaces\'"><span>View Solitaires</span>'
)

pristine_html = pristine_html.replace(
    '>GIFTING GUIDE</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">Signature Gift Sets</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Delivered in bespoke velvet keepsake vault with hallmark certificate.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html\'"><span>Discover Gift Sets</span>',
    '>ICONIC SILHOUETTE</span><h2 class="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">Austrian Tennis Bracelet</h2><p class="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">Continuous hand-set Austrian solitaires in 18K Italian gold vermeil &amp; 925 silver.</p><div class="mt-9 sm:mt-7 flex items-center gap-4"><button class="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer" onclick="window.location.href=\'products.html?category=bracelets\'"><span>Discover Bracelets</span>'
)

# Write to jewellery-design-html/index.html
with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(pristine_html)

# Check div counts
idx = pristine_html.find('data-hero-slide="0"')
s_start = pristine_html.rfind('<section', 0, idx)
s_end = pristine_html.find('</section>', idx) + 10
hero_sub = pristine_html[s_start:s_end]
open_c = hero_sub.count('<div')
close_c = hero_sub.count('</div')
print(f"Restored index.html! Hero section: open={open_c}, close={close_c}")


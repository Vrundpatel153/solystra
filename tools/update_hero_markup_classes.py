import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Build the refined, art-directed hero section markup
hero_replacement = '''  <div class="solystra-hero-wrap">
    
    <!-- Slide 0: Solitaire Heart Suite -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10 pointer-events-auto" data-hero-slide="0" id="hero-slide-0">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="inline-block text-[11px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2.5">Atelier Signature · 925 Silver</span>
            <h1 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3 drop-shadow-xs">The Solitaire Heart Suite</h1>
            <p class="text-xs sm:text-sm text-[#E8E2D9] font-light leading-relaxed mb-6">Handcrafted 925 sterling silver with brilliant Austrian solitaire heart pendant.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="px-6 py-2.5 bg-[#8E7538] hover:bg-[#725C2B] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">Explore Necklaces →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_1_pc.webp?v=solystra_art_v2026" alt="The Solitaire Heart Suite" class="w-full h-full object-cover object-center block" loading="eager" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_1_mob.webp?v=solystra_art_v2026" alt="The Solitaire Heart Suite" class="w-full h-full object-cover object-[center_top] block" loading="eager" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-16 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Atelier Signature</span>
          <h1 class="font-serif text-2xl font-normal text-white leading-tight mb-2 drop-shadow-xs">The Solitaire Heart Suite</h1>
          <p class="text-xs text-[#E8E2D9] font-light leading-relaxed mb-4">Pure 925 sterling silver with brilliant Austrian solitaire heart pendant.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="px-5 py-2.5 bg-[#8E7538] active:bg-[#725C2B] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">Explore Necklaces →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 1: Layered Pearl Solitaire -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="1" id="hero-slide-1">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="inline-block text-[11px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2.5">Couture Collection · Fine Pearls</span>
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3 drop-shadow-xs">Layered Pearl Solitaire</h2>
            <p class="text-xs sm:text-sm text-[#E8E2D9] font-light leading-relaxed mb-6">Lustrous freshwater pearls accented by dancing Austrian solitaires in handcrafted sterling silver.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="px-6 py-2.5 bg-[#8E7538] hover:bg-[#725C2B] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">Discover Pearls →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_2_pc.webp?v=solystra_art_v2026" alt="Layered Pearl Solitaire" class="w-full h-full object-cover object-center block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_2_mob.webp?v=solystra_art_v2026" alt="Layered Pearl Solitaire" class="w-full h-full object-cover object-[center_top] block" loading="lazy" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-16 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Couture Collection</span>
          <h2 class="font-serif text-2xl font-normal text-white leading-tight mb-2 drop-shadow-xs">Layered Pearl Solitaire</h2>
          <p class="text-xs text-[#E8E2D9] font-light leading-relaxed mb-4">Lustrous pearls accented by dancing Austrian solitaires.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="px-5 py-2.5 bg-[#8E7538] active:bg-[#725C2B] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">Discover Pearls →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 2: Royal Tiara Solitaire -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="2" id="hero-slide-2">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="inline-block text-[11px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2.5">Signature Atelier · 925 Silver</span>
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3 drop-shadow-xs">The Royal Tiara Solitaire</h2>
            <p class="text-xs sm:text-sm text-[#E8E2D9] font-light leading-relaxed mb-6">Bespoke tiara-cut dancing solitaire in handcrafted 925 sterling silver atelier setting.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="px-6 py-2.5 bg-[#8E7538] hover:bg-[#725C2B] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">View Solitaires →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_4_pc.webp?v=solystra_art_v2026" alt="The Royal Tiara Solitaire" class="w-full h-full object-cover object-center block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_4_mob.webp?v=solystra_art_v2026" alt="The Royal Tiara Solitaire" class="w-full h-full object-cover object-[center_top] block" loading="lazy" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-16 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Signature Atelier</span>
          <h2 class="font-serif text-2xl font-normal text-white leading-tight mb-2 drop-shadow-xs">The Royal Tiara Solitaire</h2>
          <p class="text-xs text-[#E8E2D9] font-light leading-relaxed mb-4">Bespoke tiara-cut dancing solitaire in handcrafted silver.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="px-5 py-2.5 bg-[#8E7538] active:bg-[#725C2B] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">View Solitaires →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 3: Austrian Tennis Bracelet -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="3" id="hero-slide-3">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="inline-block text-[11px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2.5">Iconic Silhouette · 18K Gold &amp; 925 Silver</span>
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3 drop-shadow-xs">Austrian Tennis Bracelet</h2>
            <p class="text-xs sm:text-sm text-[#E8E2D9] font-light leading-relaxed mb-6">Continuous hand-set Austrian solitaires in 18K Italian gold vermeil and 925 sterling silver.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=bracelets'" class="px-6 py-2.5 bg-[#8E7538] hover:bg-[#725C2B] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">Discover Bracelets →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_3_pc.webp?v=solystra_art_v2026" alt="Austrian Tennis Bracelet" class="w-full h-full object-cover object-center block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_3_mob.webp?v=solystra_art_v2026" alt="Austrian Tennis Bracelet" class="w-full h-full object-cover object-[center_top] block" loading="lazy" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-16 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Iconic Silhouette</span>
          <h2 class="font-serif text-2xl font-normal text-white leading-tight mb-2 drop-shadow-xs">Austrian Tennis Bracelet</h2>
          <p class="text-xs text-[#E8E2D9] font-light leading-relaxed mb-4">Continuous hand-set Austrian solitaires in 18K gold vermeil.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=bracelets'" class="px-5 py-2.5 bg-[#8E7538] active:bg-[#725C2B] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">Discover Bracelets →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination Dots (generous clearance from CTA button) -->
    <div class="absolute bottom-3 inset-x-0 z-30 flex justify-center gap-2 pointer-events-auto">
      <button aria-label="Slide 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs" id="hero-dot-0" onclick="window.setHeroSlide(0)"></button>
      <button aria-label="Slide 2" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-1" onclick="window.setHeroSlide(1)"></button>
      <button aria-label="Slide 3" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-2" onclick="window.setHeroSlide(2)"></button>
      <button aria-label="Slide 4" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-3" onclick="window.setHeroSlide(3)"></button>
    </div>

  </div>'''

# Match and replace the hero wrap block in index.html
pattern = r'<div class="solystra-hero-wrap">.*?<!-- Pagination Dots -->.*?</div>\s*</div>'
if re.search(pattern, content, re.DOTALL):
    new_content = re.sub(pattern, hero_replacement, content, flags=re.DOTALL)
    with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✓ Successfully replaced hero section in index.html")
else:
    print("Warning: Pattern did not match in index.html")

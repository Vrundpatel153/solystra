import re

hero_html = """<section class="relative w-full bg-[#141210] border-b border-[#2A2622] overflow-hidden">
  <div class="relative w-full h-[520px] sm:h-[480px] lg:h-[520px]">
    
    <!-- Slide 0: Solitaire Heart Suite -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10 pointer-events-auto" data-hero-slide="0" id="hero-slide-0">
      <div class="hidden sm:grid sm:grid-cols-12 h-full w-full">
        <div class="sm:col-span-6 lg:col-span-5 h-full flex flex-col justify-center px-8 sm:px-10 lg:px-14 bg-[#161412] relative z-10 border-r border-[#2C2723]/60">
          <div class="max-w-md">
            <span class="inline-block text-[10.5px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2">Atelier Signature · 925 Silver</span>
            <h1 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3">The Solitaire Heart Suite</h1>
            <p class="text-xs sm:text-sm text-[#C4BCB3] font-light leading-relaxed mb-6">Handcrafted 925 sterling silver with brilliant Austrian solitaire heart pendant.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="px-6 py-2.5 bg-[#61532E] hover:bg-[#4A3F22] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">Explore Necklaces →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="sm:col-span-6 lg:col-span-7 h-full relative overflow-hidden bg-black">
          <img src="solystra_assets/banners/hero_model_1_pc.webp?v=editorial2026" alt="The Solitaire Heart Suite" class="w-full h-full object-cover object-[center_20%] block" loading="eager" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_1_mob.webp?v=editorial2026" alt="The Solitaire Heart Suite" class="w-full h-full object-cover object-[center_12%] block" loading="eager" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-9 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Atelier Signature</span>
          <h1 class="font-serif text-2xl font-normal text-white leading-tight mb-2">The Solitaire Heart Suite</h1>
          <p class="text-xs text-stone-300 font-light leading-relaxed mb-4">Pure 925 sterling silver with brilliant Austrian solitaire heart pendant.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="px-5 py-2.5 bg-[#61532E] active:bg-[#4A3F22] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">Explore Necklaces →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 1: Layered Pearl Solitaire -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="1" id="hero-slide-1">
      <div class="hidden sm:grid sm:grid-cols-12 h-full w-full">
        <div class="sm:col-span-6 lg:col-span-5 h-full flex flex-col justify-center px-8 sm:px-10 lg:px-14 bg-[#161412] relative z-10 border-r border-[#2C2723]/60">
          <div class="max-w-md">
            <span class="inline-block text-[10.5px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2">Couture Collection · Fine Pearls</span>
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3">Layered Pearl Solitaire</h2>
            <p class="text-xs sm:text-sm text-[#C4BCB3] font-light leading-relaxed mb-6">Lustrous freshwater pearls accented by dancing Austrian solitaires in handcrafted sterling silver.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="px-6 py-2.5 bg-[#61532E] hover:bg-[#4A3F22] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">Discover Pearls →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="sm:col-span-6 lg:col-span-7 h-full relative overflow-hidden bg-black">
          <img src="solystra_assets/banners/hero_model_2_pc.webp?v=editorial2026" alt="Layered Pearl Solitaire" class="w-full h-full object-cover object-[center_20%] block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_2_mob.webp?v=editorial2026" alt="Layered Pearl Solitaire" class="w-full h-full object-cover object-[center_12%] block" loading="lazy" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-9 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Couture Collection</span>
          <h2 class="font-serif text-2xl font-normal text-white leading-tight mb-2">Layered Pearl Solitaire</h2>
          <p class="text-xs text-stone-300 font-light leading-relaxed mb-4">Lustrous pearls accented by dancing Austrian solitaires.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="px-5 py-2.5 bg-[#61532E] active:bg-[#4A3F22] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">Discover Pearls →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 2: Royal Tiara Solitaire -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="2" id="hero-slide-2">
      <div class="hidden sm:grid sm:grid-cols-12 h-full w-full">
        <div class="sm:col-span-6 lg:col-span-5 h-full flex flex-col justify-center px-8 sm:px-10 lg:px-14 bg-[#161412] relative z-10 border-r border-[#2C2723]/60">
          <div class="max-w-md">
            <span class="inline-block text-[10.5px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2">Signature Atelier · 925 Silver</span>
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3">The Royal Tiara Solitaire</h2>
            <p class="text-xs sm:text-sm text-[#C4BCB3] font-light leading-relaxed mb-6">Bespoke tiara-cut dancing solitaire in handcrafted 925 sterling silver atelier setting.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="px-6 py-2.5 bg-[#61532E] hover:bg-[#4A3F22] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">View Solitaires →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="sm:col-span-6 lg:col-span-7 h-full relative overflow-hidden bg-black">
          <img src="solystra_assets/banners/hero_model_4_pc.webp?v=editorial2026" alt="The Royal Tiara Solitaire" class="w-full h-full object-cover object-[center_20%] block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_4_mob.webp?v=editorial2026" alt="The Royal Tiara Solitaire" class="w-full h-full object-cover object-[center_12%] block" loading="lazy" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-9 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Signature Atelier</span>
          <h2 class="font-serif text-2xl font-normal text-white leading-tight mb-2">The Royal Tiara Solitaire</h2>
          <p class="text-xs text-stone-300 font-light leading-relaxed mb-4">Bespoke tiara-cut dancing solitaire in handcrafted silver.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="px-5 py-2.5 bg-[#61532E] active:bg-[#4A3F22] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">View Solitaires →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 3: Austrian Tennis Bracelet -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="3" id="hero-slide-3">
      <div class="hidden sm:grid sm:grid-cols-12 h-full w-full">
        <div class="sm:col-span-6 lg:col-span-5 h-full flex flex-col justify-center px-8 sm:px-10 lg:px-14 bg-[#161412] relative z-10 border-r border-[#2C2723]/60">
          <div class="max-w-md">
            <span class="inline-block text-[10.5px] uppercase tracking-[0.25em] text-[#D4AF37] font-semibold mb-2">Iconic Silhouette · 18K Gold Vermeil</span>
            <h2 class="font-serif text-3xl sm:text-4xl lg:text-[42px] font-normal text-white leading-[1.15] mb-3">Austrian Tennis Bracelet</h2>
            <p class="text-xs sm:text-sm text-[#C4BCB3] font-light leading-relaxed mb-6">Continuous hand-set Austrian solitaires in 18K Italian gold vermeil and 925 sterling silver.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=bracelets'" class="px-6 py-2.5 bg-[#61532E] hover:bg-[#4A3F22] text-white text-xs uppercase tracking-widest font-semibold rounded-full shadow-md transition-all cursor-pointer">Discover Bracelets →</button>
              <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] hover:text-white uppercase tracking-wider font-medium underline underline-offset-4 transition-colors cursor-pointer">Explore All</button>
            </div>
          </div>
        </div>
        <div class="sm:col-span-6 lg:col-span-7 h-full relative overflow-hidden bg-black">
          <img src="solystra_assets/banners/hero_model_3_pc.webp?v=editorial2026" alt="Austrian Tennis Bracelet" class="w-full h-full object-cover object-[center_20%] block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_3_mob.webp?v=editorial2026" alt="Austrian Tennis Bracelet" class="w-full h-full object-cover object-[center_12%] block" loading="lazy" />
        <div class="absolute inset-x-0 bottom-0 pt-20 pb-9 px-5 bg-gradient-to-t from-black/95 via-black/60 to-transparent flex flex-col justify-end text-left pointer-events-auto">
          <span class="inline-block text-[10px] uppercase tracking-[0.2em] text-[#D4AF37] font-semibold mb-1">Iconic Silhouette</span>
          <h2 class="font-serif text-2xl font-normal text-white leading-tight mb-2">Austrian Tennis Bracelet</h2>
          <p class="text-xs text-stone-300 font-light leading-relaxed mb-4">Continuous hand-set Austrian solitaires in 18K gold vermeil.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=bracelets'" class="px-5 py-2.5 bg-[#61532E] active:bg-[#4A3F22] text-white text-xs uppercase tracking-wider font-semibold rounded-full shadow cursor-pointer">Discover Bracelets →</button>
            <button onclick="window.location.href='products.html'" class="text-xs text-[#D4AF37] underline underline-offset-4 py-2 cursor-pointer">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination Dots -->
    <div class="absolute bottom-3 inset-x-0 z-20 flex justify-center gap-2">
      <button aria-label="Slide 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs" id="hero-dot-0" onclick="window.setHeroSlide(0)"></button>
      <button aria-label="Slide 2" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-1" onclick="window.setHeroSlide(1)"></button>
      <button aria-label="Slide 3" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-2" onclick="window.setHeroSlide(2)"></button>
      <button aria-label="Slide 4" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-3" onclick="window.setHeroSlide(3)"></button>
    </div>

  </div>
</section>"""

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace existing hero section
pattern = r'<section class="relative w-full overflow-hidden bg-stone-900[\s\S]*?</section>'
if re.search(pattern, content):
    new_content = re.sub(pattern, hero_html, content)
    with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully replaced Hero Section in jewellery-design-html/index.html")
else:
    print("Hero section pattern not matched! Trying broader match...")
    pos = content.find('hero-slide-0')
    start = content.rfind('<section', 0, pos)
    end = content.find('</section>', pos) + len('</section>')
    new_content = content[:start] + hero_html + content[end:]
    with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced via positional slice!")


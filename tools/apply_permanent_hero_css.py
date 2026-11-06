import re

css_block = '''
/* ==========================================================================
   Solystra Art-Directed Hero Typography, Layout & Control Rules
   ========================================================================== */
.solystra-hero-card {
  width: 44% !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  padding: 2.5rem 3rem !important;
  background: radial-gradient(circle at 20% 50%, rgba(197, 160, 89, 0.16) 0%, rgba(20, 18, 16, 0.98) 75%), #141210 !important;
  border-right: 1px solid rgba(212, 175, 55, 0.18) !important;
  position: relative !important;
  z-index: 10 !important;
  flex-shrink: 0 !important;
}

@media (min-width: 1024px) {
  .solystra-hero-card {
    padding: 3rem 4rem !important;
    width: 42% !important;
  }
}

.solystra-hero-card .hero-tag,
.solystra-hero-mob-overlay .hero-tag {
  color: #D4AF37 !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.25em !important;
  margin-bottom: 0.65rem !important;
  display: block !important;
}

.solystra-hero-card h1,
.solystra-hero-card h2 {
  color: #FFFFFF !important;
  font-family: Georgia, serif !important;
  font-size: 38px !important;
  font-weight: 400 !important;
  line-height: 1.15 !important;
  margin-bottom: 0.85rem !important;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6) !important;
}

.solystra-hero-card p {
  color: #F0ECE4 !important;
  font-size: 14px !important;
  font-weight: 300 !important;
  line-height: 1.6 !important;
  margin-bottom: 1.75rem !important;
  max-width: 420px !important;
}

.solystra-hero-card .hero-cta-btn {
  background-color: #8E7538 !important;
  color: #FFFFFF !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.15em !important;
  padding: 0.75rem 1.75rem !important;
  border-radius: 9999px !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
  transition: all 0.3s ease !important;
  cursor: pointer !important;
  border: 1px solid rgba(212, 175, 55, 0.35) !important;
  display: inline-block !important;
}

.solystra-hero-card .hero-cta-btn:hover {
  background-color: #A38744 !important;
  box-shadow: 0 6px 20px rgba(163, 135, 68, 0.35) !important;
  transform: translateY(-1px) !important;
}

.solystra-hero-card .hero-secondary-btn {
  color: #D4AF37 !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  text-decoration: underline !important;
  text-underline-offset: 4px !important;
  cursor: pointer !important;
  transition: color 0.2s ease !important;
  background: none !important;
  border: none !important;
}

.solystra-hero-card .hero-secondary-btn:hover {
  color: #FFFFFF !important;
}

/* Mobile Hero Overlay & Separation from Dots */
.solystra-hero-mob-overlay {
  position: absolute !important;
  inset-x: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  padding-top: 5rem !important;
  padding-bottom: 4.5rem !important; /* 72px padding: button NEVER collides with dots! */
  padding-left: 1.25rem !important;
  padding-right: 1.25rem !important;
  background: linear-gradient(to top, rgba(10, 8, 7, 0.96) 0%, rgba(10, 8, 7, 0.65) 55%, transparent 100%) !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-end !important;
  text-align: left !important;
  pointer-events: auto !important;
  z-index: 15 !important;
}

.solystra-hero-mob-overlay h1,
.solystra-hero-mob-overlay h2 {
  color: #FFFFFF !important;
  font-family: Georgia, serif !important;
  font-size: 24px !important;
  font-weight: 400 !important;
  line-height: 1.2 !important;
  margin-bottom: 0.4rem !important;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.7) !important;
}

.solystra-hero-mob-overlay p {
  color: #F0ECE4 !important;
  font-size: 12px !important;
  font-weight: 300 !important;
  line-height: 1.5 !important;
  margin-bottom: 1rem !important;
}

.solystra-hero-mob-overlay .hero-cta-btn {
  background-color: #8E7538 !important;
  color: #FFFFFF !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  padding: 0.65rem 1.4rem !important;
  border-radius: 9999px !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
  cursor: pointer !important;
  border: 1px solid rgba(212, 175, 55, 0.35) !important;
}

.solystra-hero-dots {
  position: absolute !important;
  bottom: 0.85rem !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 30 !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 0.5rem !important;
  pointer-events: auto !important;
}
'''

with open('jewellery-design-html/css/styles.css', 'a', encoding='utf-8') as f:
    f.write(css_block)

print("✓ Appended art-directed hero rules to styles.css")

# Now update index.html with the refined classes
hero_html = '''  <div class="solystra-hero-wrap">
    
    <!-- Slide 0: Solitaire Heart Suite -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10 pointer-events-auto" data-hero-slide="0" id="hero-slide-0">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="hero-tag">Atelier Signature · 925 Silver</span>
            <h1>The Solitaire Heart Suite</h1>
            <p>Handcrafted 925 sterling silver with brilliant Austrian solitaire heart pendant.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="hero-cta-btn">Explore Necklaces →</button>
              <button onclick="window.location.href='products.html'" class="hero-secondary-btn">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_1_pc.webp?v=solystra_art_v2026_fixed" alt="The Solitaire Heart Suite" class="w-full h-full object-cover object-center block" loading="eager" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_1_mob.webp?v=solystra_art_v2026_fixed" alt="The Solitaire Heart Suite" class="w-full h-full object-cover object-center block" loading="eager" />
        <div class="solystra-hero-mob-overlay">
          <span class="hero-tag">Atelier Signature</span>
          <h1>The Solitaire Heart Suite</h1>
          <p>Pure 925 sterling silver with brilliant Austrian solitaire heart pendant.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="hero-cta-btn">Explore Necklaces →</button>
            <button onclick="window.location.href='products.html'" class="hero-secondary-btn">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 1: Layered Pearl Solitaire -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="1" id="hero-slide-1">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="hero-tag">Couture Collection · Fine Pearls</span>
            <h2>Layered Pearl Solitaire</h2>
            <p>Lustrous freshwater pearls accented by dancing Austrian solitaires in handcrafted sterling silver.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="hero-cta-btn">Discover Pearls →</button>
              <button onclick="window.location.href='products.html'" class="hero-secondary-btn">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_2_pc.webp?v=solystra_art_v2026_fixed" alt="Layered Pearl Solitaire" class="w-full h-full object-cover object-center block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_2_mob.webp?v=solystra_art_v2026_fixed" alt="Layered Pearl Solitaire" class="w-full h-full object-cover object-center block" loading="lazy" />
        <div class="solystra-hero-mob-overlay">
          <span class="hero-tag">Couture Collection</span>
          <h2>Layered Pearl Solitaire</h2>
          <p>Lustrous pearls accented by dancing Austrian solitaires.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="hero-cta-btn">Discover Pearls →</button>
            <button onclick="window.location.href='products.html'" class="hero-secondary-btn">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 2: Royal Tiara Solitaire -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="2" id="hero-slide-2">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="hero-tag">Signature Atelier · 925 Silver</span>
            <h2>The Royal Tiara Solitaire</h2>
            <p>Bespoke tiara-cut dancing solitaire in handcrafted 925 sterling silver atelier setting.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=necklaces'" class="hero-cta-btn">View Solitaires →</button>
              <button onclick="window.location.href='products.html'" class="hero-secondary-btn">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_4_pc.webp?v=solystra_art_v2026_fixed" alt="The Royal Tiara Solitaire" class="w-full h-full object-cover object-center block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_4_mob.webp?v=solystra_art_v2026_fixed" alt="The Royal Tiara Solitaire" class="w-full h-full object-cover object-center block" loading="lazy" />
        <div class="solystra-hero-mob-overlay">
          <span class="hero-tag">Signature Atelier</span>
          <h2>The Royal Tiara Solitaire</h2>
          <p>Bespoke tiara-cut dancing solitaire in handcrafted silver.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=necklaces'" class="hero-cta-btn">View Solitaires →</button>
            <button onclick="window.location.href='products.html'" class="hero-secondary-btn">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Slide 3: Austrian Tennis Bracelet -->
    <div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="3" id="hero-slide-3">
      <div class="solystra-hero-desktop-grid">
        <div class="solystra-hero-card">
          <div class="max-w-md">
            <span class="hero-tag">Iconic Silhouette · 18K Gold &amp; 925 Silver</span>
            <h2>Austrian Tennis Bracelet</h2>
            <p>Continuous hand-set Austrian solitaires in 18K Italian gold vermeil and 925 sterling silver.</p>
            <div class="flex items-center gap-4">
              <button onclick="window.location.href='products.html?category=bracelets'" class="hero-cta-btn">Discover Bracelets →</button>
              <button onclick="window.location.href='products.html'" class="hero-secondary-btn">Explore All</button>
            </div>
          </div>
        </div>
        <div class="solystra-hero-img-col">
          <img src="solystra_assets/banners/hero_model_3_pc.webp?v=solystra_art_v2026_fixed" alt="Austrian Tennis Bracelet" class="w-full h-full object-cover object-center block" loading="lazy" />
        </div>
      </div>
      <div class="sm:hidden relative w-full h-full overflow-hidden bg-black">
        <img src="solystra_assets/banners/hero_model_3_mob.webp?v=solystra_art_v2026_fixed" alt="Austrian Tennis Bracelet" class="w-full h-full object-cover object-center block" loading="lazy" />
        <div class="solystra-hero-mob-overlay">
          <span class="hero-tag">Iconic Silhouette</span>
          <h2>Austrian Tennis Bracelet</h2>
          <p>Continuous hand-set Austrian solitaires in 18K gold vermeil.</p>
          <div class="flex items-center gap-3">
            <button onclick="window.location.href='products.html?category=bracelets'" class="hero-cta-btn">Discover Bracelets →</button>
            <button onclick="window.location.href='products.html'" class="hero-secondary-btn">View All</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination Dots (generous clearance from CTA button) -->
    <div class="solystra-hero-dots">
      <button aria-label="Slide 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs" id="hero-dot-0" onclick="window.setHeroSlide(0)"></button>
      <button aria-label="Slide 2" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-1" onclick="window.setHeroSlide(1)"></button>
      <button aria-label="Slide 3" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-2" onclick="window.setHeroSlide(2)"></button>
      <button aria-label="Slide 4" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70" id="hero-dot-3" onclick="window.setHeroSlide(3)"></button>
    </div>

  </div>'''

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

pattern = r'<div class="solystra-hero-wrap">.*?<!-- Pagination Dots.*?</div>\s*</div>'
if re.search(pattern, idx_content, re.DOTALL):
    idx_content = re.sub(pattern, hero_html, idx_content, flags=re.DOTALL)
    with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
        f.write(idx_content)
    print("✓ Successfully updated index.html with art-directed hero markup")

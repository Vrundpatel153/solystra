with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Slide 2 class in index.html
old_slide_2 = '<div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10" data-hero-slide="2" id="hero-slide-2">'
new_slide_2 = '<div class="absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none" data-hero-slide="2" id="hero-slide-2">'

assert old_slide_2 in html, "Could not find old_slide_2 in index.html"
html = html.replace(old_slide_2, new_slide_2)

# 2. Add fetchpriority="high" to Slide 0 image
old_slide_0_img = '<img alt="The 18K Gold Suite" class="w-full h-full object-cover object-center block" loading="eager" src="solystra_assets/banners/banner_pc_2.webp"/>'
new_slide_0_img = '<img alt="The 18K Gold Suite" class="w-full h-full object-cover object-center block" loading="eager" fetchpriority="high" src="solystra_assets/banners/banner_pc_2.webp"/>'

if old_slide_0_img in html:
    html = html.replace(old_slide_0_img, new_slide_0_img)
    print("Updated Slide 0 img with fetchpriority='high'")

# 3. Add preload tags to <head> if not already present
preload_tags = '''<link rel="preload" as="image" href="solystra_assets/banners/banner_pc_2.webp" media="(min-width: 641px)" fetchpriority="high"/>
<link rel="preload" as="image" href="solystra_assets/banners/banner_mob_2.webp" media="(max-width: 640px)" fetchpriority="high"/>'''

if 'banner_pc_2.webp" media="(min-width: 641px)"' not in html:
    pos_head = html.find('</head>')
    html = html[:pos_head] + preload_tags + '\n' + html[pos_head:]
    print("Added hero banner preloads to <head>")

with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated jewellery-design-html/index.html successfully!")

# 4. Update js/app.js
with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_js_block = """    // Hero Carousel Slider Controller
  let currentHeroSlide = 2; // Default: Modern Classics
  window.setHeroSlide = function (idx) {
    currentHeroSlide = idx;
    for (let i = 0; i < 4; i++) {
      const slide = document.getElementById(`hero-slide-${i}`);
      const dot = document.getElementById(`hero-dot-${i}`);
      if (slide) {
        if (i === idx) {
          slide.className = 'absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10';
        } else {
          slide.className = 'absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none';
        }
      }
      if (dot) {
        if (i === idx) {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs';
        } else {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70';
        }
      }
    }
  };

  window.heroCarouselInterval = setInterval(() => {
    const next = (currentHeroSlide + 1) % 4;
    window.setHeroSlide(next);
  }, 5500);"""

new_js_block = """    // Hero Carousel Slider Controller
  let currentHeroSlide = 0; // Default: Slide 0 (The 18K Gold Suite)
  window.setHeroSlide = function (idx) {
    currentHeroSlide = idx;
    for (let i = 0; i < 4; i++) {
      const slide = document.getElementById(`hero-slide-${i}`);
      const dot = document.getElementById(`hero-dot-${i}`);
      if (slide) {
        if (i === idx) {
          slide.className = 'absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10 pointer-events-auto';
        } else {
          slide.className = 'absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none';
        }
      }
      if (dot) {
        if (i === idx) {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs';
        } else {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70';
        }
      }
    }
  };

  // Defensively sync slide 0 on initial execution
  if (typeof document !== 'undefined') {
    window.setHeroSlide(0);
  }

  if (window.heroCarouselInterval) {
    clearInterval(window.heroCarouselInterval);
  }
  window.heroCarouselInterval = setInterval(() => {
    const next = (currentHeroSlide + 1) % 4;
    window.setHeroSlide(next);
  }, 5500);"""

assert old_js_block in js, "Could not find old_js_block in app.js"
js = js.replace(old_js_block, new_js_block)

with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated jewellery-design-html/js/app.js successfully!")


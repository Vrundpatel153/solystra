import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# The 8 official reels
REELS = [
  {
    "id": "reel-1",
    "title": "Aura Solitaire Drop Pendant",
    "category": "necklaces",
    "metal": "18K Gold & Pure 925 Silver",
    "price": 2799,
    "mrp": 3999,
    "videoSrc": "solystra_assets/videos/reel_01_DaFwwDoSUFL.mp4",
    "productImage": "solystra_assets/videos/posters/poster_01_DaFwwDoSUFL.webp",
    "instagramUrl": "https://www.instagram.com/reel/DaFwwDoSUFL/",
    "desc": "Jewellery that moves with you — designed with intention, lightweight, balanced, and quietly elegant."
  },
  {
    "id": "reel-2",
    "title": "Everyday Ease Solitaire Necklace",
    "category": "necklaces",
    "metal": "BIS-Hallmarked Real Gold",
    "price": 3299,
    "mrp": 4599,
    "videoSrc": "solystra_assets/videos/reel_02_DaiPSBhyTkV.mp4",
    "productImage": "solystra_assets/videos/posters/poster_02_DaiPSBhyTkV.webp",
    "instagramUrl": "https://www.instagram.com/reel/DaiPSBhyTkV/",
    "desc": "Designed for ease, shaped by simplicity, and crafted to move with you through every moment."
  },
  {
    "id": "reel-3",
    "title": "Timeless Heirloom Solitaire Suite",
    "category": "necklaces",
    "metal": "Pure 925 Silver & 18K Gold",
    "price": 4499,
    "mrp": 6299,
    "videoSrc": "solystra_assets/videos/reel_03_DaVVXNOSQxw.mp4",
    "productImage": "solystra_assets/videos/posters/poster_03_DaVVXNOSQxw.webp",
    "instagramUrl": "https://www.instagram.com/reel/DaVVXNOSQxw/",
    "desc": "Some pieces don’t just complete a look, they become a part of your story."
  },
  {
    "id": "reel-4",
    "title": "Daily Luxe Effortless Gold Chain",
    "category": "necklaces",
    "metal": "18K Italian Gold Polish",
    "price": 2999,
    "mrp": 4199,
    "videoSrc": "solystra_assets/videos/reel_04_DYtkml_yz66.mp4",
    "productImage": "solystra_assets/videos/posters/poster_04_DYtkml_yz66.webp",
    "instagramUrl": "https://www.instagram.com/reel/DYtkml_yz66/",
    "desc": "Everyday gold, but make it effortless. Clean, minimal, polished, and designed for daily wear."
  },
  {
    "id": "reel-5",
    "title": "The Solystra Signature Infinity Set",
    "category": "complete_sets",
    "metal": "BIS-Hallmarked Gold & Solitaire",
    "price": 4999,
    "mrp": 6999,
    "videoSrc": "solystra_assets/videos/reel_05_DYhd6MnysBj.mp4",
    "productImage": "solystra_assets/videos/posters/poster_05_DYhd6MnysBj.webp",
    "instagramUrl": "https://www.instagram.com/reel/DYhd6MnysBj/",
    "desc": "The Infinity Set by Solystra. Minimal, lightweight, timeless, and perfect for everyday wear."
  },
  {
    "id": "reel-6",
    "title": "Waveproof Tarnish-Free Link Bracelet",
    "category": "bracelets",
    "metal": "Waterproof Dual-Micron Rhodium",
    "price": 2499,
    "mrp": 3499,
    "videoSrc": "solystra_assets/videos/reel_06_DZXkay2y6VU.mp4",
    "productImage": "solystra_assets/videos/posters/poster_06_DZXkay2y6VU.webp",
    "instagramUrl": "https://www.instagram.com/reel/DZXkay2y6VU/",
    "desc": "Waterproof, sweatproof, and tarnish-free summer brilliance that moves with the waves."
  },
  {
    "id": "reel-7",
    "title": "Versatile 3-in-1 Pendant Suite",
    "category": "necklaces",
    "metal": "925 Sterling Silver & Solitaires",
    "price": 3899,
    "mrp": 5499,
    "videoSrc": "solystra_assets/videos/reel_07_DavF6Jlyvwd.mp4",
    "productImage": "solystra_assets/videos/posters/poster_07_DavF6Jlyvwd.webp",
    "instagramUrl": "https://www.instagram.com/reel/DavF6Jlyvwd/",
    "desc": "Three looks. One collection. Endless ways to make it yours — from everyday to gala nights."
  },
  {
    "id": "reel-8",
    "title": "Festive Gala Solitaire Earrings",
    "category": "earrings",
    "metal": "18K Gold Vermeil & Solitaires",
    "price": 2899,
    "mrp": 3999,
    "videoSrc": "solystra_assets/videos/reel_08_DegrYkoKQrI.mp4",
    "productImage": "solystra_assets/videos/posters/poster_08_DegrYkoKQrI.webp",
    "instagramUrl": "https://www.instagram.com/reel/DegrYkoKQrI/",
    "desc": "Some jewellery is too good to stay off the camera roll. Your festive fits with Solystra sparkle."
  }
]

def render_card_html(reel, loop_num):
    return f"""<div class="w-[205px] sm:w-[235px] md:w-[255px] shrink-0 group relative rounded-2xl overflow-hidden bg-white border border-[#CEBDA7] hover:border-[#61532E]/60 shadow-xs hover:shadow-xl transition-all duration-300 flex flex-col">
  <div class="aspect-[4/5] relative overflow-hidden bg-stone-950 cursor-pointer" onclick="window.location.href='products.html?category={reel['category']}'">
    <video muted="" autoplay="" class="w-full h-full object-cover block group-hover:scale-105 transition-transform duration-500 pointer-events-none" loop="" playsinline="" poster="{reel['productImage']}" src="{reel['videoSrc']}"></video>
    <div class="absolute inset-0 bg-black/0 group-hover:bg-black/15 transition-colors pointer-events-none"></div>
    <a href="{reel['instagramUrl']}" target="_blank" rel="noopener noreferrer" class="absolute top-2.5 right-2.5 z-10 px-2 py-1 rounded-full bg-black/60 hover:bg-[#61532E] backdrop-blur-md text-white text-[9.5px] font-medium flex items-center gap-1 transition-all border border-white/20 shadow-xs cursor-pointer group/ig" title="View Reel on Instagram" onclick="event.stopPropagation()">
      <svg class="w-2.5 h-2.5 fill-current text-pink-400 group-hover/ig:text-white" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
      <span>Reel</span>
    </a>
  </div>
  <div class="p-3 sm:p-3.5 bg-white flex flex-col gap-2.5">
    <div class="flex items-center gap-2.5">
      <div class="w-11 h-11 sm:w-12 sm:h-12 rounded-xl bg-stone-50 border border-stone-200 overflow-hidden shrink-0 shadow-2xs cursor-pointer hover:opacity-90 transition-opacity" onclick="window.location.href='products.html?category={reel['category']}'">
        <img alt="{reel['title']}" class="w-full h-full object-cover" loading="lazy" src="{reel['productImage']}"/>
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-xs sm:text-[12.5px] font-semibold text-stone-900 truncate cursor-pointer hover:text-[#61532E] transition-colors leading-tight" onclick="window.location.href='products.html?category={reel['category']}'" title="{reel['title']}">{reel['title']}</p>
        <p class="text-[10px] sm:text-[10.5px] text-stone-500 font-medium truncate mt-0.5">{reel['metal']}</p>
      </div>
      <div class="text-right shrink-0">
        <span class="text-xs sm:text-[13px] font-bold text-[#61532E] block">₹{reel['price']:,}</span>
        <span class="text-[9.5px] text-stone-400 line-through block -mt-0.5">₹{reel['mrp']:,}</span>
      </div>
    </div>
    <div class="pt-2 border-t border-[#F0EBE3]">
      <button class="w-full py-2 px-2.5 rounded-lg bg-[#61532E] hover:bg-[#3D341B] text-white font-sans text-xs font-semibold flex items-center justify-center gap-1.5 transition-all duration-150 cursor-pointer active:scale-95 shadow-2xs group/video-cart" onclick="window.handleVideoAddToCart &amp;&amp; window.handleVideoAddToCart('{reel['id']}')" title="Add to Cart" type="button">
        <svg aria-hidden="true" class="w-3.5 h-3.5 shrink-0 -translate-y-px transition-transform duration-200 group-hover/video-cart:-translate-y-0.5" fill="none" viewbox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M6 2L3 6V20C3 21.1 3.9 22 5 22H19C20.1 22 21 21.1 21 20V6L18 2H6Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><path d="M3 6H21" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><path d="M16 10C16 12.21 14.21 14 12 14C9.79 14 8 12.21 8 10" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
        <span class="truncate tracking-wide leading-none">Add to Cart</span>
      </button>
    </div>
  </div>
</div>"""

# Tripled list for infinite looping marquee
all_cards_html = []
for loop in range(1, 4):
    for r in REELS:
        all_cards_html.append(render_card_html(r, loop))

full_reels_inner_html = "".join(all_cards_html)

def update_html_file(fpath):
    if not os.path.exists(fpath):
        print("Not found:", fpath)
        return
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<div id="video-reels-scroll" class="flex flex-nowrap gap-4 sm:gap-5 overflow-x-auto hide-scrollbar pb-4 pt-1 cursor-grab active:cursor-grabbing select-none">'
    end_tag = '</div></div></section>'
    
    idx = content.find(start_tag)
    if idx == -1:
        # try without select-none or with other classes
        idx = content.find('id="video-reels-scroll"')
        if idx == -1:
            print("video-reels-scroll not found in:", fpath)
            return
        tag_end = content.find('>', idx) + 1
        content_end = content.find(end_tag, tag_end)
        content = content[:tag_end] + full_reels_inner_html + content[content_end:]
    else:
        tag_end = idx + len(start_tag)
        content_end = content.find(end_tag, tag_end)
        content = content[:tag_end] + full_reels_inner_html + content[content_end:]
        
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated HTML:", fpath)

# Update HTML files
update_html_file('jewellery-design-html/index.html')
update_html_file('jewellery-design-html-dist/index.html')
update_html_file(r'c:\Users\vrund\OneDrive\Desktop\solystra-html\index.html')

# Update React HomePage.jsx
react_path = 'src/pages/HomePage.jsx'
if os.path.exists(react_path):
    with open(react_path, 'r', encoding='utf-8') as f:
        r_content = f.read()
    
    # Generate new VIDEO_REELS array for React
    import json
    react_reels_code = "const VIDEO_REELS = [\n"
    for r in REELS:
        react_reels_code += f"""  {{
    id: '{r['id']}',
    title: '{r['title']}',
    category: '{r['category']}',
    metal: '{r['metal']}',
    price: {r['price']},
    mrp: {r['mrp']},
    videoSrc: '{r['videoSrc']}',
    productImage: '{r['productImage']}',
    instagramUrl: '{r['instagramUrl']}',
    desc: '{r['desc']}'
  }},\n"""
    react_reels_code = react_reels_code.rstrip(',\n') + "\n];"
    
    idx_reels = r_content.find('const VIDEO_REELS = [')
    end_reels = r_content.find('];', idx_reels) + 2
    r_content = r_content[:idx_reels] + react_reels_code + r_content[end_reels:]
    
    with open(react_path, 'w', encoding='utf-8') as f:
        f.write(r_content)
    print("Updated React HomePage.jsx")

print("All updates completed successfully!")

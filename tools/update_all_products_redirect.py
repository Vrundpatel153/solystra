import re

desktop_old = """<!-- Explore All Categories Link --><button class="w-full text-left py-2 px-2.5 rounded-xl hover:bg-[#F6F3EE] transition-all cursor-pointer group flex items-center justify-between pt-2 border-t border-[#CEBDA7]/60" onclick="window.location.href='categories.html'"><div class="text-[12px] font-semibold text-[#61532E] group-hover:text-[#3D341B] flex items-center gap-1.5"><span>Explore All Categories Archive</span><svg class="lucide lucide-chevron-right w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg></div></button>"""

desktop_new = """<!-- Explore All Products Link (Direct Redirect to All Products Page) -->
<button class="w-full text-left py-2.5 px-3 rounded-xl bg-gradient-to-r from-[#FAF8F5] via-white to-[#F6F3EE] hover:from-[#61532E] hover:to-[#4A3F22] text-[#61532E] hover:text-white border border-[#CEBDA7] hover:border-[#61532E] transition-all duration-300 cursor-pointer group flex items-center justify-between shadow-xs mt-2" onclick="window.location.href='products.html'">
  <div class="flex items-center gap-2.5">
    <div class="w-6 h-6 rounded-lg bg-[#61532E]/10 group-hover:bg-white/20 flex items-center justify-center transition-colors shrink-0">
      <svg class="w-3.5 h-3.5 text-[#61532E] group-hover:text-white transition-colors" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"></path></svg>
    </div>
    <div>
      <div class="text-[12.5px] font-sans font-bold leading-tight flex items-center gap-1.5">
        <span>Explore All Products</span>
        <span class="text-[8.5px] px-1.5 py-0.2 rounded-full bg-[#61532E]/10 group-hover:bg-white/20 text-[#61532E] group-hover:text-white font-semibold transition-colors">143+</span>
      </div>
      <div class="text-[10px] text-stone-500 group-hover:text-white/80 font-light mt-0.5">Browse entire atelier collection</div>
    </div>
  </div>
  <svg class="lucide lucide-chevron-right w-4 h-4 text-[#61532E]/60 group-hover:text-white group-hover:translate-x-1 transition-all" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg>
</button>
<!-- Explore All Categories Archive Link -->
<button class="w-full text-left py-1.5 px-2.5 rounded-xl hover:bg-[#F6F3EE] transition-all cursor-pointer group flex items-center justify-between text-stone-600 hover:text-[#3D341B] mt-1" onclick="window.location.href='categories.html'">
  <div class="text-[11.5px] font-medium flex items-center gap-1.5">
    <svg class="lucide lucide-layout-grid w-3 h-3 text-[#61532E]/70" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><rect height="7" rx="1" width="7" x="3" y="3"></rect><rect height="7" rx="1" width="7" x="14" y="3"></rect><rect height="7" rx="1" width="7" x="14" y="14"></rect><rect height="7" rx="1" width="7" x="3" y="14"></rect></svg>
    <span>Explore All Categories Archive</span>
  </div>
  <svg class="lucide lucide-chevron-right w-3.5 h-3.5 text-stone-300 group-hover:text-[#61532E] group-hover:translate-x-0.5 transition-transform" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg>
</button>"""

mobile_old = """<button class="w-full p-2.5 bg-[#F6F3EE] rounded-lg border border-[#61532E]/20 text-center text-xs font-semibold text-[#61532E] hover:bg-[#EFEAE3] transition-colors cursor-pointer flex items-center justify-center gap-1.5 mt-1" onclick="window.location.href='categories.html'"><span>Explore All Categories Archive</span><svg class="lucide lucide-chevron-right w-3.5 h-3.5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg></button>"""

mobile_new = """<button class="w-full p-2.5 bg-gradient-to-r from-[#FAF8F5] to-white hover:from-[#61532E] hover:to-[#4A3F22] hover:text-white rounded-xl border border-[#CEBDA7] text-left text-xs font-semibold text-[#61532E] transition-all cursor-pointer flex items-center justify-between shadow-2xs mt-2 group" onclick="window.location.href='products.html'">
  <div class="flex items-center gap-2">
    <svg class="w-3.5 h-3.5 text-[#61532E] group-hover:text-white transition-colors" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"></path></svg>
    <span>Explore All Products (143+ Creations)</span>
  </div>
  <svg class="lucide lucide-chevron-right w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg>
</button>
<button class="w-full p-2 bg-[#F6F3EE] rounded-lg border border-[#61532E]/20 text-center text-xs font-medium text-stone-600 hover:text-[#61532E] hover:bg-[#EFEAE3] transition-colors cursor-pointer flex items-center justify-center gap-1.5 mt-1.5" onclick="window.location.href='categories.html'">
  <span>Explore All Categories Archive</span>
  <svg class="lucide lucide-chevron-right w-3 h-3 text-stone-400" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg>
</button>"""

files_to_update = [
    'jewellery-design-html/index.html',
    'jewellery-design-html/products.html',
    'jewellery-design-html/product.html',
    'jewellery-design-html/categories.html',
    'jewellery-design-html/offers.html',
    'jewellery-design-html/privacy.html',
    'jewellery-design-html/terms.html'
]

for fpath in files_to_update:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    d_count = content.count(desktop_old)
    m_count = content.count(mobile_old)
    print(f"{fpath}: desktop match={d_count}, mobile match={m_count}")
    
    if d_count > 0:
        content = content.replace(desktop_old, desktop_new)
    if m_count > 0:
        content = content.replace(mobile_old, mobile_new)
        
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  -> Updated {fpath}")

# Also update breadcrumb in product.html
with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    pdp_content = f.read()

crumb_old = """<a class="hover:text-[#61532E] transition-colors" href="index.html">Home</a><svg class="lucide lucide-chevron-right w-3 h-3 text-stone-300" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg><a class="capitalize hover:text-[#61532E] transition-colors" href="products.html?category=necklaces" id="pdp-crumb-cat">"""

crumb_new = """<a class="hover:text-[#61532E] transition-colors" href="index.html">Home</a><svg class="lucide lucide-chevron-right w-3 h-3 text-stone-300" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg><a class="hover:text-[#61532E] transition-colors font-medium text-stone-700" href="products.html">All Products</a><svg class="lucide lucide-chevron-right w-3 h-3 text-stone-300" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg><a class="capitalize hover:text-[#61532E] transition-colors" href="products.html?category=necklaces" id="pdp-crumb-cat">"""

if crumb_old in pdp_content:
    pdp_content = pdp_content.replace(crumb_old, crumb_new)
    with open('jewellery-design-html/product.html', 'w', encoding='utf-8') as f:
        f.write(pdp_content)
    print("  -> Updated product.html breadcrumb with 'All Products' link")
else:
    print("  -> Warning: crumb_old not found in product.html, let's inspect")

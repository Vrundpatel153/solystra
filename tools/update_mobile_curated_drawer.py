import os
import re

files = [
    'jewellery-design-html/index.html',
    'jewellery-design-html/products.html',
    'jewellery-design-html/categories.html',
    'jewellery-design-html/offers.html',
    'jewellery-design-html/product.html'
]

old_pattern = re.compile(
    r'<div class="space-y-1 pb-3 border-b border-\[#CEBDA7\]">\s*'
    r'<div class="text-\[11px\] font-bold uppercase tracking-wider text-\[#61532E\] mb-1\.5">Curated Collections</div>\s*'
    r'<div class="grid grid-cols-1 gap-1">[\s\S]*?</div>\s*</div>',
    re.MULTILINE
)

new_accordion_html = '''<!-- Mobile Curated Collections Accordion -->
<div class="rounded-xl border border-[#CEBDA7] bg-white overflow-hidden shadow-2xs mb-2">
  <button class="w-full flex items-center justify-between p-2.5 bg-[#FAF8F5] text-left cursor-pointer active:bg-[#F6F3EE] transition-colors" onclick="window.toggleCategoryDropdown('mob-curated', event)" type="button">
    <div class="flex items-center gap-2">
      <span class="w-3.5 h-3.5 rounded-full border border-white shrink-0 shadow-xs" style="background: linear-gradient(135deg, #F3E8D6 0%, #C5A059 50%, #61532E 100%);"></span>
      <div>
        <div class="text-xs font-bold text-stone-900 flex items-center gap-1.5">
          <span>Curated Collections</span>
          <span class="text-[8.5px] px-1.5 py-0.2 rounded bg-white text-[#61532E] border border-[#CEBDA7]/80 font-bold uppercase">Signature</span>
        </div>
        <div class="text-[9.5px] text-stone-400">Links, Drops, Daily Luxe &amp; Tennis</div>
      </div>
    </div>
    <div class="flex items-center gap-1">
      <svg class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 transition-transform duration-300" id="chevron-mob-curated" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m6 9 6 6 6-6"></path></svg>
    </div>
  </button>
  <div class="space-y-0.5 p-2 bg-white border-t border-[#CEBDA7]/60 hidden" id="subcat-menu-mob-curated">
    <button class="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer group" onclick="window.location.href='products.html?category=necklaces'">
      <div class="flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
        <span class="text-stone-800 group-hover:text-[#61532E] font-medium">Links &amp; Layers</span>
      </div>
      <span class="text-[10px] text-stone-400 font-light">Chains, chokers &amp; links</span>
    </button>
    <button class="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer group" onclick="window.location.href='products.html?category=earrings'">
      <div class="flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
        <span class="text-stone-800 group-hover:text-[#61532E] font-medium">Drops &amp; Halo</span>
      </div>
      <span class="text-[10px] text-stone-400 font-light">Halo rings &amp; drops</span>
    </button>
    <button class="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer group" onclick="window.location.href='products.html?category=anklets'">
      <div class="flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
        <span class="text-stone-800 group-hover:text-[#61532E] font-medium">Dainty Steps</span>
      </div>
      <span class="text-[10px] text-stone-400 font-light">Dainty anklets &amp; charms</span>
    </button>
    <button class="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer group" onclick="window.location.href='products.html?metal=gold'">
      <div class="flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
        <span class="text-stone-800 group-hover:text-[#61532E] font-medium">Daily Luxe</span>
      </div>
      <span class="text-[10px] text-stone-400 font-light">18K gold everyday</span>
    </button>
    <button class="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer group" onclick="window.location.href='products.html?category=bracelets'">
      <div class="flex items-center gap-2">
        <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
        <span class="text-stone-800 group-hover:text-[#61532E] font-medium">Tennis Fever</span>
      </div>
      <span class="text-[10px] text-stone-400 font-light">Tennis bracelets &amp; cuffs</span>
    </button>
  </div>
</div>'''

for fn in files:
    if os.path.exists(fn):
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, count = old_pattern.subn(new_accordion_html, content)
        print(f"{fn}: Replaced {count} occurrences")
        if count > 0:
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(new_content)


import re

def polish_top_row():
    path = 'jewellery-design-html/products.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Refine desktop control row
    old_row_start = html.find('<div class="hidden lg:flex items-center justify-between pb-4 mb-6 border-b border-[#CEBDA7]/70 gap-4">')
    old_row_end = html.find('<!-- Mobile Control Stack', old_row_start)
    
    refined_desktop_row = """<div class="hidden lg:flex items-center justify-between pb-4 mb-6 border-b border-[#CEBDA7]/70 gap-3 xl:gap-4">
  <!-- Left: Title & Count -->
  <div class="flex items-center gap-2 shrink-0">
    <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
    <span class="text-xs font-semibold text-stone-900 tracking-wide uppercase">Curated Handcrafted Collection</span>
    <span id="catalog-products-count" class="text-xs text-stone-400 font-light">(143 creations)</span>
  </div>

  <!-- Middle: Quick Price Filter Pills -->
  <div class="flex items-center gap-1 xl:gap-1.5 shrink-0" id="desktop-price-pills">
    <button type="button" data-price-range="all" class="px-2.5 xl:px-3 py-1.5 rounded-xl text-[11.5px] xl:text-xs transition-all cursor-pointer font-semibold bg-[#61532E] text-white shadow-2xs">All Prices</button>
    <button type="button" data-price-range="under-3000" class="px-2.5 xl:px-3 py-1.5 rounded-xl text-[11.5px] xl:text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">Under ₹3,000</button>
    <button type="button" data-price-range="3000-7000" class="px-2.5 xl:px-3 py-1.5 rounded-xl text-[11.5px] xl:text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">₹3,000 – ₹7,000</button>
    <button type="button" data-price-range="7000-15000" class="px-2.5 xl:px-3 py-1.5 rounded-xl text-[11.5px] xl:text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">₹7,000 – ₹15,000</button>
    <button type="button" data-price-range="15000-30000" class="px-2.5 xl:px-3 py-1.5 rounded-xl text-[11.5px] xl:text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">₹15,000 – ₹30,000</button>
    <button type="button" data-price-range="above-30000" class="px-2.5 xl:px-3 py-1.5 rounded-xl text-[11.5px] xl:text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">Above ₹30,000</button>
  </div>

  <!-- Right: Filter Popup Button + Sort Dropdown Side-by-Side -->
  <div class="flex items-center gap-2 shrink-0 pl-2.5 border-l border-[#CEBDA7]/70">
    <!-- Filter Popup Button with Sliders Icon -->
    <button type="button" onclick="window.openFilterModal()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#CEBDA7] bg-[#FAF8F5] hover:bg-[#F5F0EA] active:scale-95 text-stone-800 text-xs font-semibold shadow-2xs transition-all cursor-pointer group">
      <svg class="lucide lucide-sliders-horizontal w-3.5 h-3.5 text-[#61532E] group-hover:scale-110 transition-transform" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><line x1="21" x2="14" y1="4" y2="4"></line><line x1="10" x2="3" y1="4" y2="4"></line><line x1="21" x2="12" y1="12" y2="12"></line><line x1="8" x2="3" y1="12" y2="12"></line><line x1="21" x2="16" y1="20" y2="20"></line><line x1="12" x2="3" y1="20" y2="20"></line><line x1="14" x2="14" y1="2" y2="6"></line><line x1="8" x2="8" y1="10" y2="14"></line><line x1="16" x2="16" y1="18" y2="22"></line></svg>
      <span>Filter</span>
      <span id="desktop-filter-count-badge" class="hidden px-1.5 py-0.5 rounded-full bg-[#61532E] text-white text-[10px] font-bold leading-none"></span>
    </button>

    <!-- Sort Dropdown -->
    <div class="relative" id="desktop-sort-wrapper">
      <button id="desktop-sort-btn" onclick="window.toggleDesktopSortMenu && window.toggleDesktopSortMenu(event)" aria-expanded="false" aria-haspopup="listbox" class="flex items-center justify-between gap-1.5 bg-[#FAF8F5] hover:bg-[#F5F0EA] border text-stone-800 text-xs font-semibold rounded-xl transition-all cursor-pointer shadow-2xs border-[#CEBDA7] px-3 py-1.5 min-w-[130px]" type="button">
        <span class="text-stone-400 font-light mr-0.5">Sort:</span>
        <span class="truncate" id="desktop-sort-label">Featured</span>
        <svg class="lucide lucide-chevron-down w-3.5 h-3.5 transition-transform duration-200 shrink-0 text-stone-500" id="desktop-sort-chevron" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="m6 9 6 6 6-6"></path></svg>
      </button>
      <div id="desktop-sort-dropdown" class="hidden absolute right-0 mt-1.5 w-44 bg-white border border-[#CEBDA7] rounded-xl shadow-xl py-1.5 z-50 animate-fadeIn">
        <button type="button" onclick="window.setSortOption('featured')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Featured</span><span class="text-[#61532E] font-bold sort-check" data-sort-val="featured">✓</span></button>
        <button type="button" onclick="window.setSortOption('price-low')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Price: Low to High</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="price-low">✓</span></button>
        <button type="button" onclick="window.setSortOption('price-high')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Price: High to Low</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="price-high">✓</span></button>
        <button type="button" onclick="window.setSortOption('rating')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Customer Rating</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="rating">✓</span></button>
        <button type="button" onclick="window.setSortOption('newest')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Newest First</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="newest">✓</span></button>
      </div>
    </div>
  </div>
</div>
"""

    if old_row_start != -1 and old_row_end != -1:
        html = html[:old_row_start] + refined_desktop_row + html[old_row_end:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Refined desktop top row in products.html.")

if __name__ == '__main__':
    polish_top_row()


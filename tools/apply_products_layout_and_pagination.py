import re

def transform_products_html():
    html_path = 'jewellery-design-html/products.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove the sticky mobile bar section that had duplicate filter/sort buttons if present
    # Look for <section class="lg:hidden bg-white/95 backdrop-blur-md border-b border-[#CEBDA7] sticky solystra-nav-overlay...
    old_mobile_sticky_sec = re.search(r'<section class="lg:hidden bg-white/95 backdrop-blur-md border-b border-\[#CEBDA7\] sticky solystra-nav-overlay.*?<\/section>', html, re.DOTALL)
    if old_mobile_sticky_sec:
        print("Found old mobile sticky section (length %d), removing it to integrate cleanly." % len(old_mobile_sticky_sec.group(0)))
        html = html[:old_mobile_sticky_sec.start()] + html[old_mobile_sticky_sec.end():]

    # 2. Find <aside ...>...</aside> and the outer <div class="flex gap-8 items-start">
    # Let's locate from '<div class="flex gap-8 items-start">' to '<main class="flex-1 min-w-0">'
    flex_aside_match = re.search(r'<div class="flex gap-8 items-start">\s*<aside class="hidden lg:block w-64.*?<\/aside>\s*<main class="flex-1 min-w-0">', html, re.DOTALL)
    if flex_aside_match:
        print("Found <aside> wrapper match (length %d)" % len(flex_aside_match.group(0)))
        html = html[:flex_aside_match.start()] + '<main class="w-full">' + html[flex_aside_match.end():]
    else:
        print("WARNING: Could not find exact flex gap-8 + aside regex match!")

    # 3. Replace the top control bar inside <main>
    # The old top bar was:
    # <div class="hidden lg:flex items-center justify-between pb-3.5 mb-4 border-b border-[#CEBDA7]">...</div>
    old_top_bar_match = re.search(r'<div class="hidden lg:flex items-center justify-between pb-3\.5 mb-4 border-b border-\[#CEBDA7\]">.*?<\/div>\s*<\/div>\s*<\/div>', html, re.DOTALL)
    if not old_top_bar_match:
        # Try broader search
        old_top_bar_match = re.search(r'<div class="hidden lg:flex items-center justify-between.*?<\/div>\s*<\/div>\s*<\/div>', html, re.DOTALL)
    
    desktop_mobile_controls = """<!-- Unified Catalog Controls -->
<!-- Desktop Control Row (Single Full Line) -->
<div class="hidden lg:flex items-center justify-between pb-4 mb-6 border-b border-[#CEBDA7]/70 gap-4">
  <!-- Left: Title & Count -->
  <div class="flex items-center gap-2 shrink-0">
    <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
    <span class="text-xs font-semibold text-stone-900 tracking-wide uppercase">Curated Handcrafted Collection</span>
    <span id="catalog-products-count" class="text-xs text-stone-400 font-light">(143 creations)</span>
  </div>

  <!-- Middle: Quick Price Filter Pills -->
  <div class="flex items-center gap-1.5 shrink-0" id="desktop-price-pills">
    <button type="button" data-price-range="all" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-semibold bg-[#61532E] text-white shadow-2xs">All Prices</button>
    <button type="button" data-price-range="under-3000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">Under ₹3,000</button>
    <button type="button" data-price-range="3000-7000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">₹3,000 – ₹7,000</button>
    <button type="button" data-price-range="7000-15000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">₹7,000 – ₹15,000</button>
    <button type="button" data-price-range="15000-30000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">₹15,000 – ₹30,000</button>
    <button type="button" data-price-range="above-30000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/40">Above ₹30,000</button>
  </div>

  <!-- Right: Filter Popup Button + Sort Dropdown Side-by-Side -->
  <div class="flex items-center gap-2.5 shrink-0 pl-3 border-l border-[#CEBDA7]/70">
    <!-- Filter Popup Button with Sliders Icon -->
    <button type="button" onclick="window.openFilterModal()" class="flex items-center gap-2 px-3.5 py-1.5 rounded-xl border border-[#CEBDA7] bg-[#FAF8F5] hover:bg-[#F5F0EA] active:scale-95 text-stone-800 text-xs font-semibold shadow-2xs transition-all cursor-pointer group">
      <svg class="lucide lucide-sliders-horizontal w-3.5 h-3.5 text-[#61532E] group-hover:scale-110 transition-transform" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><line x1="21" x2="14" y1="4" y2="4"></line><line x1="10" x2="3" y1="4" y2="4"></line><line x1="21" x2="12" y1="12" y2="12"></line><line x1="8" x2="3" y1="12" y2="12"></line><line x1="21" x2="16" y1="20" y2="20"></line><line x1="12" x2="3" y1="20" y2="20"></line><line x1="14" x2="14" y1="2" y2="6"></line><line x1="8" x2="8" y1="10" y2="14"></line><line x1="16" x2="16" y1="18" y2="22"></line></svg>
      <span>Filter</span>
      <span id="desktop-filter-count-badge" class="hidden px-1.5 py-0.5 rounded-full bg-[#61532E] text-white text-[10px] font-bold leading-none"></span>
    </button>

    <!-- Sort Dropdown -->
    <div class="relative" id="desktop-sort-wrapper">
      <button id="desktop-sort-btn" onclick="window.toggleDesktopSortMenu && window.toggleDesktopSortMenu(event)" aria-expanded="false" aria-haspopup="listbox" class="flex items-center justify-between gap-2 bg-[#FAF8F5] hover:bg-[#F5F0EA] border text-stone-800 text-xs font-semibold rounded-xl transition-all cursor-pointer shadow-2xs border-[#CEBDA7] px-3.5 py-1.5 min-w-[145px]" type="button">
        <span class="text-stone-400 font-light mr-0.5">Sort:</span>
        <span class="truncate" id="desktop-sort-label">Featured</span>
        <svg class="lucide lucide-chevron-down w-3.5 h-3.5 transition-transform duration-200 shrink-0 text-stone-500" id="desktop-sort-chevron" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="m6 9 6 6 6-6"></path></svg>
      </button>
      <div id="desktop-sort-dropdown" class="hidden absolute right-0 mt-1.5 w-48 bg-white border border-[#CEBDA7] rounded-xl shadow-xl py-1.5 z-50 animate-fadeIn">
        <button type="button" onclick="window.setSortOption('featured')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Featured</span><span class="text-[#61532E] font-bold sort-check" data-sort-val="featured">✓</span></button>
        <button type="button" onclick="window.setSortOption('price-low')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Price: Low to High</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="price-low">✓</span></button>
        <button type="button" onclick="window.setSortOption('price-high')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Price: High to Low</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="price-high">✓</span></button>
        <button type="button" onclick="window.setSortOption('rating')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Customer Rating</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="rating">✓</span></button>
        <button type="button" onclick="window.setSortOption('newest')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Newest First</span><span class="text-[#61532E] font-bold sort-check hidden" data-sort-val="newest">✓</span></button>
      </div>
    </div>
  </div>
</div>

<!-- Mobile Control Stack (Properly Aligned for Mobile View) -->
<div class="lg:hidden pb-4 mb-4 space-y-2.5">
  <!-- Row 1: Title and count -->
  <div class="flex items-center justify-between px-1">
    <div class="flex items-center gap-1.5">
      <span class="w-1.5 h-1.5 rounded-full bg-[#61532E]"></span>
      <span class="text-xs font-semibold text-stone-900 tracking-wide uppercase">Curated Atelier Collection</span>
    </div>
    <span id="mobile-catalog-products-count" class="text-xs text-stone-400 font-light">(143 creations)</span>
  </div>

  <!-- Row 2: Horizontally scrollable quick price pills -->
  <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1 -mx-1 px-1" id="mobile-price-pills">
    <button type="button" data-price-range="all" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-semibold whitespace-nowrap bg-[#61532E] text-white shadow-2xs shrink-0">All Prices</button>
    <button type="button" data-price-range="under-3000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium whitespace-nowrap bg-white border border-[#CEBDA7] text-stone-700 shrink-0">Under ₹3,000</button>
    <button type="button" data-price-range="3000-7000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium whitespace-nowrap bg-white border border-[#CEBDA7] text-stone-700 shrink-0">₹3,000 – ₹7,000</button>
    <button type="button" data-price-range="7000-15000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium whitespace-nowrap bg-white border border-[#CEBDA7] text-stone-700 shrink-0">₹7,000 – ₹15,000</button>
    <button type="button" data-price-range="15000-30000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium whitespace-nowrap bg-white border border-[#CEBDA7] text-stone-700 shrink-0">₹15,000 – ₹30,000</button>
    <button type="button" data-price-range="above-30000" class="px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium whitespace-nowrap bg-white border border-[#CEBDA7] text-stone-700 shrink-0">Above ₹30,000</button>
  </div>

  <!-- Row 3: 50/50 Side-by-Side Filter & Sort Controls -->
  <div class="grid grid-cols-2 gap-2.5 pt-0.5">
    <button type="button" onclick="window.openFilterModal()" class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl border border-[#CEBDA7] bg-[#FAF8F5] hover:bg-[#F5F0EA] active:scale-[0.98] text-xs font-semibold text-stone-800 shadow-2xs transition-all cursor-pointer">
      <svg class="lucide lucide-sliders-horizontal w-3.5 h-3.5 text-[#61532E]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><line x1="21" x2="14" y1="4" y2="4"></line><line x1="10" x2="3" y1="4" y2="4"></line><line x1="21" x2="12" y1="12" y2="12"></line><line x1="8" x2="3" y1="12" y2="12"></line><line x1="21" x2="16" y1="20" y2="20"></line><line x1="12" x2="3" y1="20" y2="20"></line><line x1="14" x2="14" y1="2" y2="6"></line><line x1="8" x2="8" y1="10" y2="14"></line><line x1="16" x2="16" y1="18" y2="22"></line></svg>
      <span>Filters</span>
      <span id="mobile-filter-count-badge" class="hidden px-1.5 py-0.5 rounded-full bg-[#61532E] text-white text-[10px] font-bold leading-none"></span>
    </button>
    <div class="relative w-full" id="mobile-sort-wrapper">
      <button id="mobile-sort-btn" onclick="window.toggleMobileSortMenu && window.toggleMobileSortMenu(event)" aria-expanded="false" aria-haspopup="listbox" class="w-full flex items-center justify-between gap-2 bg-[#FAF8F5] hover:bg-[#F5F0EA] border text-stone-800 text-xs font-semibold rounded-xl transition-all cursor-pointer shadow-2xs border-[#CEBDA7] py-2 px-3" type="button">
        <span class="truncate" id="mobile-sort-label">Featured</span>
        <svg class="lucide lucide-chevron-down w-3.5 h-3.5 transition-transform duration-200 shrink-0 text-stone-500" id="mobile-sort-chevron" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="m6 9 6 6 6-6"></path></svg>
      </button>
      <div id="mobile-sort-dropdown" class="hidden absolute right-0 mt-1.5 w-full bg-white border border-[#CEBDA7] rounded-xl shadow-xl py-1.5 z-50 animate-fadeIn">
        <button type="button" onclick="window.setSortOption('featured')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Featured</span><span class="text-[#61532E] font-bold mobile-sort-check" data-sort-val="featured">✓</span></button>
        <button type="button" onclick="window.setSortOption('price-low')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Price: Low to High</span><span class="text-[#61532E] font-bold mobile-sort-check hidden" data-sort-val="price-low">✓</span></button>
        <button type="button" onclick="window.setSortOption('price-high')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Price: High to Low</span><span class="text-[#61532E] font-bold mobile-sort-check hidden" data-sort-val="price-high">✓</span></button>
        <button type="button" onclick="window.setSortOption('rating')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Customer Rating</span><span class="text-[#61532E] font-bold mobile-sort-check hidden" data-sort-val="rating">✓</span></button>
        <button type="button" onclick="window.setSortOption('newest')" class="w-full text-left px-3.5 py-2 text-xs font-medium text-stone-700 hover:bg-[#FAF8F5] hover:text-[#61532E] transition-colors flex items-center justify-between cursor-pointer"><span>Newest First</span><span class="text-[#61532E] font-bold mobile-sort-check hidden" data-sort-val="newest">✓</span></button>
      </div>
    </div>
  </div>
</div>
"""

    if old_top_bar_match:
        print("Found old top bar match, replacing...")
        html = html[:old_top_bar_match.start()] + desktop_mobile_controls + html[old_top_bar_match.end():]
    else:
        print("WARNING: Could not find old top bar match!")

    # 4. Update products grid class from 4 cols to 5 cols
    # Find id="products-catalog-grid" class="..."
    grid_match = re.search(r'(<div[^>]*id="products-catalog-grid"[^>]*class=")([^"]*)(")', html)
    if grid_match:
        print("Found grid match. Old class:", grid_match.group(2))
        new_grid_class = "grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-5 gap-3 sm:gap-4 md:gap-5"
        html = html[:grid_match.start(2)] + new_grid_class + html[grid_match.end(2):]
    else:
        print("WARNING: Could not find id='products-catalog-grid' class")

    # 5. Add Pagination Container right after #products-catalog-grid closes
    # Find closing of products-catalog-grid and </main>
    # Note: after all 143 cards, there is the closing </div> of products-catalog-grid
    pagination_html = """
<!-- Catalog Pagination Bar -->
<div id="catalog-pagination-container" class="mt-10 sm:mt-12 pt-6 border-t border-[#CEBDA7]/70 flex flex-col sm:flex-row items-center justify-between gap-4">
  <!-- Left: Showing summary -->
  <div class="text-xs text-stone-500 font-light" id="catalog-pagination-summary">
    Showing <span class="font-semibold text-stone-800" id="pagination-start-range">1</span>–<span class="font-semibold text-stone-800" id="pagination-end-range">20</span> of <span class="font-semibold text-stone-800" id="pagination-total-items">143</span> creations
  </div>

  <!-- Center/Right: Pagination Controls -->
  <nav aria-label="Catalog Pagination" class="flex items-center gap-1.5 sm:gap-2">
    <!-- Previous Button -->
    <button type="button" id="pagination-prev-btn" onclick="window.changeCatalogPage(window.getCurrentCatalogPage() - 1)" class="flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-[#CEBDA7] bg-white hover:bg-[#FAF8F5] text-xs font-semibold text-stone-700 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-white transition-all cursor-pointer shadow-2xs">
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"></path></svg>
      <span>Previous</span>
    </button>

    <!-- Page Number Buttons (rendered dynamically) -->
    <div id="pagination-pages-list" class="flex items-center gap-1 sm:gap-1.5">
      <!-- Injected by app.js -->
    </div>

    <!-- Next Button -->
    <button type="button" id="pagination-next-btn" onclick="window.changeCatalogPage(window.getCurrentCatalogPage() + 1)" class="flex items-center gap-1.5 px-3.5 py-2 rounded-xl border border-[#CEBDA7] bg-white hover:bg-[#FAF8F5] text-xs font-semibold text-stone-700 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-white transition-all cursor-pointer shadow-2xs">
      <span>Next</span>
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"></path></svg>
    </button>
  </nav>
</div>
"""
    # Locate where </main> is
    pos_main_end = html.find('</main>')
    if pos_main_end != -1:
        print("Found </main> at", pos_main_end)
        html = html[:pos_main_end] + pagination_html + html[pos_main_end:]
    else:
        print("WARNING: Could not find </main>")

    # Clean up closing tags if the outer flex wrapper div was removed
    # If we changed `<div class="flex gap-8 items-start">` to `<main class="w-full">`, we need to make sure the matching closing `</div>` after `</main>` is removed.
    # Let's inspect after `</main>`:
    # Was: `</main></div></div></div>` -> now should be `</main></div></div>`
    pos_after_main = html.find('</main>') + len('</main>')
    closing_snippet = html[pos_after_main:pos_after_main+50]
    print("Closing snippet after </main>:", repr(closing_snippet))
    if closing_snippet.startswith('</div></div></div>'):
        html = html[:pos_after_main] + '</div></div>' + html[pos_after_main + len('</div></div></div>'):]
        print("Adjusted closing divs.")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully transformed products.html!")

if __name__ == '__main__':
    transform_products_html()


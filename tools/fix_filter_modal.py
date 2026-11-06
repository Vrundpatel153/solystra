import re

with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_func_start = text.find('window.openMobileFilterModal = function () {')
assert old_func_start != -1, "Could not find window.openMobileFilterModal"

# Find end of closeMobileFilterModal
old_func_end = text.find('// Size Guide Modal', old_func_start)
assert old_func_end != -1, "Could not find Size Guide Modal anchor"

new_code = """window.openMobileFilterModal = function () {
    let m = document.getElementById('mobile-filter-modal');
    if (!m) {
      m = document.createElement('div');
      m.id = 'mobile-filter-modal';
      m.className = 'fixed inset-0 z-[100] bg-black/75 backdrop-blur-xs flex items-center justify-center font-sans p-2.5 sm:p-4 overflow-hidden';
      m.onclick = function (e) {
        if (e.target === m) {
          window.closeMobileFilterModal();
        }
      };
      m.innerHTML = `
        <div class="bg-white w-full max-w-lg rounded-2xl sm:rounded-3xl shadow-2xl border border-[#CEBDA7]/70 flex flex-col overflow-hidden animate-slide-up" style="max-height: calc(100dvh - 20px); height: min(760px, calc(100dvh - 20px));">
          
          <!-- 1. STICKY TOP HEADER (Always visible, never scrolls out of view) -->
          <div class="flex-shrink-0 flex items-center justify-between px-4 sm:px-6 py-3.5 sm:py-4 border-b border-[#CEBDA7]/60 bg-[#FAF8F5] z-10 select-none">
            <div class="flex items-center gap-2.5 min-w-0">
              <div class="w-8 h-8 rounded-full bg-[#61532E]/10 flex items-center justify-center text-[#61532E] shrink-0">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="21" x2="14" y1="4" y2="4"></line><line x1="10" x2="3" y1="4" y2="4"></line><line x1="21" x2="12" y1="12" y2="12"></line><line x1="8" x2="3" y1="12" y2="12"></line><line x1="21" x2="16" y1="20" y2="20"></line><line x1="12" x2="3" y1="20" y2="20"></line><line x1="14" x2="14" y1="2" y2="6"></line><line x1="8" x2="8" y1="10" y2="14"></line><line x1="16" x2="16" y1="18" y2="22"></line></svg>
              </div>
              <div class="min-w-0">
                <h3 class="font-serif text-base sm:text-lg font-semibold text-stone-900 leading-tight truncate">Filter Atelier Creations</h3>
                <p class="text-[11px] text-stone-500 font-light mt-0.5 truncate">Select multiple categories, finishes &amp; curated collections</p>
              </div>
            </div>
            <button type="button" onclick="window.closeMobileFilterModal()" class="w-8.5 h-8.5 rounded-full bg-white hover:bg-stone-100 border border-[#CEBDA7]/70 flex items-center justify-center text-stone-500 hover:text-stone-900 transition-all cursor-pointer active:scale-95 shadow-2xs shrink-0 ml-2" aria-label="Close filters">
              <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>

          <!-- 2. SCROLLABLE MIDDLE BODY (Effortless smooth scrolling with visible luxury scrollbar) -->
          <div class="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4 text-xs overscroll-contain" style="scrollbar-width: thin; scrollbar-color: #CEBDA7 #FAF8F5; -webkit-overflow-scrolling: touch;">
            
            <!-- 0. Max Budget Slider -->
            <div class="rounded-xl border border-[#CEBDA7]/70 bg-[#FAF8F5]/80 p-3.5 shadow-2xs space-y-2">
              <div class="flex items-center justify-between">
                <span class="font-bold text-stone-800 uppercase tracking-wider text-[11px]">Max Budget</span>
                <span id="modal-budget-display" class="font-bold text-xs text-[#61532E]">₹80,000</span>
              </div>
              <input type="range" id="modal-budget-slider" min="1000" max="80000" step="1000" value="80000" oninput="window.setModalMaxPrice(this.value)" class="w-full accent-[#61532E] cursor-pointer" />
              <div class="flex items-center justify-between text-[10px] text-stone-400 font-light">
                <span>₹1,000</span>
                <span>₹80,000+</span>
              </div>
            </div>

            <!-- 1. Category -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="font-bold text-stone-800 uppercase tracking-wider">Category</span>
                <span class="text-[10px] text-stone-400">Multi-selectable</span>
              </div>
              <div class="grid grid-cols-2 gap-2" id="mobile-filter-categories">
                <button type="button" data-filter-cat="all" onclick="window.toggleMobileFilterCategory('all')">All Creations</button>
                <button type="button" data-filter-cat="bracelets" onclick="window.toggleMobileFilterCategory('bracelets')">Bracelets &amp; Kadas</button>
                <button type="button" data-filter-cat="necklaces" onclick="window.toggleMobileFilterCategory('necklaces')">Necklaces &amp; Pendants</button>
                <button type="button" data-filter-cat="rings" onclick="window.toggleMobileFilterCategory('rings')">Rings &amp; Bands</button>
                <button type="button" data-filter-cat="earrings" onclick="window.toggleMobileFilterCategory('earrings')">Earrings &amp; Studs</button>
                <button type="button" data-filter-cat="complete_sets" onclick="window.toggleMobileFilterCategory('complete_sets')">Gift Sets &amp; Suites</button>
              </div>
            </div>

            <!-- 2. Precious Finish -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="font-bold text-stone-800 uppercase tracking-wider">Precious Finish</span>
                <span class="text-[10px] text-stone-400">Multi-selectable</span>
              </div>
              <div class="grid grid-cols-2 gap-2" id="mobile-filter-metals">
                <button type="button" data-filter-metal="all" onclick="window.toggleMobileFilterMetal('all')">All Finishes</button>
                <button type="button" data-filter-metal="silver" onclick="window.toggleMobileFilterMetal('silver')">Pure 925 Silver</button>
                <button type="button" data-filter-metal="gold" onclick="window.toggleMobileFilterMetal('gold')">18K Gold Vermeil</button>
                <button type="button" data-filter-metal="rose" onclick="window.toggleMobileFilterMetal('rose')">18K Rose Gold</button>
              </div>
            </div>

            <!-- 3. Curated Collections Accordion -->
            <div class="rounded-xl border border-[#CEBDA7]/70 bg-[#FAF8F5]/80 overflow-hidden shadow-2xs">
              <button type="button" onclick="window.toggleModalCuratedDropdown()" class="w-full flex items-center justify-between p-3 text-left cursor-pointer active:bg-[#F6F3EE] transition-colors" aria-expanded="false">
                <div class="flex items-center gap-2.5">
                  <span class="w-3.5 h-3.5 rounded-full border border-white shrink-0 shadow-xs" style="background: linear-gradient(135deg, #F3E8D6 0%, #C5A059 50%, #61532E 100%);"></span>
                  <div>
                    <span class="font-bold text-stone-900 uppercase tracking-wider text-[11px] block">Curated Collections</span>
                    <span class="text-[9.5px] text-stone-400 font-light block mt-0.5">Tap to expand curated suites &amp; links</span>
                  </div>
                </div>
                <div class="flex items-center gap-1.5">
                  <span class="hidden" id="modal-curated-summary"></span>
                  <svg class="w-4 h-4 text-stone-500 transition-transform duration-300" id="chevron-modal-curated" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"></path></svg>
                </div>
              </button>
              <div id="modal-curated-container" class="space-y-1.5 p-3 bg-white border-t border-[#CEBDA7]/60 hidden overflow-hidden transition-all duration-300">
                <div class="grid grid-cols-2 gap-2" id="mobile-filter-curated">
                  <button type="button" data-filter-curated="links_layers" onclick="window.toggleMobileFilterCurated('links_layers')">Links &amp; Layers</button>
                  <button type="button" data-filter-curated="drops_halo" onclick="window.toggleMobileFilterCurated('drops_halo')">Drops &amp; Halo</button>
                  <button type="button" data-filter-curated="dainty_steps" onclick="window.toggleMobileFilterCurated('dainty_steps')">Dainty Steps</button>
                  <button type="button" data-filter-curated="daily_luxe" onclick="window.toggleMobileFilterCurated('daily_luxe')">Daily Luxe</button>
                  <button type="button" data-filter-curated="tennis_fever" onclick="window.toggleMobileFilterCurated('tennis_fever')">Tennis Fever</button>
                  <button type="button" data-filter-curated="heirloom_suites" onclick="window.toggleMobileFilterCurated('heirloom_suites')">Heirloom Suites</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 3. STICKY BOTTOM FOOTER (Always visible, never scrolls out of view) -->
          <div class="flex-shrink-0 p-3 sm:p-4 border-t border-[#CEBDA7]/60 bg-[#FAF8F5] grid grid-cols-2 gap-3 z-10 shadow-[0_-4px_16px_rgba(0,0,0,0.04)] select-none">
            <button type="button" onclick="window.resetMobileFiltersAndClose()" class="w-full py-2.5 sm:py-3 px-3 border border-[#CEBDA7] hover:border-stone-400 bg-white hover:bg-stone-50 rounded-xl text-xs font-semibold text-stone-700 active:scale-95 transition-all text-center flex items-center justify-center cursor-pointer shadow-xs">Reset Filters</button>
            <button type="button" onclick="window.applyMobileFiltersAndClose()" class="w-full py-2.5 sm:py-3 px-3 bg-[#61532E] hover:bg-[#4A3F22] text-white rounded-xl text-xs font-bold uppercase tracking-wider active:scale-95 transition-all shadow-md text-center flex items-center justify-center cursor-pointer">Apply Filters</button>
          </div>
        </div>
      `;
      document.body.appendChild(m);
    }

    // Sync temporary state with current filter state
    const current = window.getCatalogFilterState ? window.getCatalogFilterState() : { categories: ['all'], metals: ['all'], curated: [] };
    window._tempMobileCategories = new Set(current.categories);
    window._tempMobileMetals = new Set(current.metals);
    window._tempMobileCurated = new Set(current.curated || []);
    window._renderMobileFilterPillStates();

    // Lock background scroll
    document.body.style.overflow = 'hidden';

    // Keydown ESC listener
    window._filterModalEscHandler = function (e) {
      if (e.key === 'Escape') {
        window.closeMobileFilterModal();
      }
    };
    window.addEventListener('keydown', window._filterModalEscHandler);

    m.classList.remove('hidden');
  };

  window.closeMobileFilterModal = function () {
    const m = document.getElementById('mobile-filter-modal');
    if (m) m.classList.add('hidden');
    document.body.style.overflow = '';
    if (window._filterModalEscHandler) {
      window.removeEventListener('keydown', window._filterModalEscHandler);
    }
  };

  """

text = text[:old_func_start] + new_code + text[old_func_end:]

with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated jewellery-design-html/js/app.js with bulletproof 3-tier filter modal!")

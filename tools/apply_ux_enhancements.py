import os
import re

print("Starting UX enhancements implementation...")

# 1. UPDATE app.js
app_js_path = 'jewellery-design-html/js/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js = f.read()

# A. Enhance toggleCategoryDropdown to smoothly support curated along with silver & gold
old_toggle = """  window.toggleCategoryDropdown = function (key, e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const subMenu = document.getElementById('subcat-menu-' + key);
    const chevron = document.getElementById('chevron-' + key);
    if (!subMenu) return;

    const prefix = key.startsWith('mob-') ? 'mob-' : 'desktop-';
    const otherKey = prefix + (key.endsWith('silver') ? 'gold' : 'silver');
    const otherMenu = document.getElementById('subcat-menu-' + otherKey);
    const otherChevron = document.getElementById('chevron-' + otherKey);"""

new_toggle = """  window.toggleCategoryDropdown = function (key, e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const subMenu = document.getElementById('subcat-menu-' + key);
    const chevron = document.getElementById('chevron-' + key);
    if (!subMenu) return;

    const prefix = key.startsWith('mob-') ? 'mob-' : 'desktop-';
    const allKeys = ['curated', 'silver', 'gold'];
    allKeys.forEach(function (k) {
      const otherKey = prefix + k;
      if (otherKey !== key) {
        const otherMenu = document.getElementById('subcat-menu-' + otherKey);
        const otherChevron = document.getElementById('chevron-' + otherKey);
        closeAccordion(otherMenu, otherChevron);
      }
    });"""

if old_toggle in app_js:
    app_js = app_js.replace(old_toggle, new_toggle)
    print("Updated toggleCategoryDropdown in app.js successfully!")
else:
    print("WARNING: old_toggle pattern not found in app.js, checking regex...")

# B. Update initProductsPage filter states and multi-select support
old_filter_states = """    // Filter states
    const params = new URLSearchParams(window.location.search);
    let activeCategory = (params.get('category') || 'all').toLowerCase();
    let activeMetal = (params.get('metal') || 'all').toLowerCase();
    let activeFilter = (params.get('filter') || 'all').toLowerCase();"""

new_filter_states = """    // Filter states (supports single or multi-select array)
    const params = new URLSearchParams(window.location.search);
    const rawCat = (params.get('category') || 'all').toLowerCase();
    let activeCategories = rawCat.split(',').map(s => s.trim()).filter(Boolean);
    if (activeCategories.length === 0) activeCategories = ['all'];
    let activeCategory = activeCategories[0] || 'all';

    const rawMetal = (params.get('metal') || 'all').toLowerCase();
    let activeMetals = rawMetal.split(',').map(s => s.trim()).filter(Boolean);
    if (activeMetals.length === 0) activeMetals = ['all'];
    let activeMetal = activeMetals[0] || 'all';

    let activeFilter = (params.get('filter') || 'all').toLowerCase();"""

if old_filter_states in app_js:
    app_js = app_js.replace(old_filter_states, new_filter_states)
    print("Updated filter states for multi-select in app.js successfully!")
else:
    print("WARNING: old_filter_states not found in app.js")

# C. Update matching in applyFilters()
old_cat_match = """        // Category match
        let catMatch = false;
        if (activeCategory === 'all') {
          catMatch = true;
        } else if (activeCategory === 'bestseller' || activeCategory === 'bestsellers') {
          catMatch = isBestseller;
        } else if (activeCategory === 'new') {
          catMatch = isNew;
        } else if (activeCategory === 'complete_sets' || activeCategory === 'gift sets & suites' || activeCategory === 'sets') {
          catMatch = cat === 'complete_sets' || cat === 'sets' || name.includes('set') || name.includes('suite');
        } else if (activeCategory === 'layering chains' || activeCategory === 'chains') {
          catMatch = cat === 'necklaces' && (name.includes('chain') || name.includes('lariat'));
        } else if (activeCategory === 'silver anklets' || activeCategory === 'anklets') {
          catMatch = cat === 'anklets' || name.includes('anklet');
        } else if (activeCategory === 'bracelets & kadas' || activeCategory === 'bracelets') {
          catMatch = cat === 'bracelets' || name.includes('bracelet') || name.includes('bangle') || name.includes('cuff') || name.includes('kada');
        } else if (activeCategory === 'necklaces & pendants' || activeCategory === 'necklaces') {
          catMatch = cat === 'necklaces' || name.includes('necklace') || name.includes('pendant');
        } else if (activeCategory === 'rings & bands' || activeCategory === 'rings') {
          catMatch = cat === 'rings' || name.includes('ring') || name.includes('band') || name.includes('solitaire');
        } else if (activeCategory === 'earrings & studs' || activeCategory === 'earrings') {
          catMatch = cat === 'earrings' || name.includes('earring') || name.includes('stud') || name.includes('hoop') || name.includes('drop');
        } else {
          catMatch = cat.includes(activeCategory) || activeCategory.includes(cat);
        }

        // Metal match
        let metalMatch = false;
        if (activeMetal === 'all') {
          metalMatch = true;
        } else if (activeMetal === 'silver' || activeMetal === '925 silver') {
          metalMatch = metal === 'silver';
        } else if (activeMetal === 'gold' || activeMetal === '18k gold') {
          metalMatch = metal === 'gold';
        } else if (activeMetal === 'rose' || activeMetal === 'rose gold') {
          metalMatch = metal === 'rose';
        }"""

new_cat_match = """        // Helper for category matching
        function testSingleCat(cTarget) {
          if (cTarget === 'all') return true;
          if (cTarget === 'bestseller' || cTarget === 'bestsellers') return isBestseller;
          if (cTarget === 'new') return isNew;
          if (cTarget === 'complete_sets' || cTarget === 'gift sets & suites' || cTarget === 'sets') {
            return cat === 'complete_sets' || cat === 'sets' || name.includes('set') || name.includes('suite');
          }
          if (cTarget === 'layering chains' || cTarget === 'chains') {
            return cat === 'necklaces' && (name.includes('chain') || name.includes('lariat'));
          }
          if (cTarget === 'silver anklets' || cTarget === 'anklets') {
            return cat === 'anklets' || name.includes('anklet');
          }
          if (cTarget === 'bracelets & kadas' || cTarget === 'bracelets') {
            return cat === 'bracelets' || name.includes('bracelet') || name.includes('bangle') || name.includes('cuff') || name.includes('kada');
          }
          if (cTarget === 'necklaces & pendants' || cTarget === 'necklaces') {
            return cat === 'necklaces' || name.includes('necklace') || name.includes('pendant');
          }
          if (cTarget === 'rings & bands' || cTarget === 'rings') {
            return cat === 'rings' || name.includes('ring') || name.includes('band') || name.includes('solitaire');
          }
          if (cTarget === 'earrings & studs' || cTarget === 'earrings') {
            return cat === 'earrings' || name.includes('earring') || name.includes('stud') || name.includes('hoop') || name.includes('drop');
          }
          return cat.includes(cTarget) || cTarget.includes(cat);
        }

        // Helper for metal matching
        function testSingleMetal(mTarget) {
          if (mTarget === 'all') return true;
          if (mTarget === 'silver' || mTarget === '925 silver') return metal === 'silver';
          if (mTarget === 'gold' || mTarget === '18k gold') return metal === 'gold';
          if (mTarget === 'rose' || mTarget === 'rose gold') return metal === 'rose';
          return metal.includes(mTarget) || mTarget.includes(metal);
        }

        // Multi-select Category match
        let catMatch = false;
        if (activeCategories.includes('all') || activeCategories.length === 0) {
          catMatch = true;
        } else {
          catMatch = activeCategories.some(c => testSingleCat(c));
        }

        // Multi-select Metal match
        let metalMatch = false;
        if (activeMetals.includes('all') || activeMetals.length === 0) {
          metalMatch = true;
        } else {
          metalMatch = activeMetals.some(m => testSingleMetal(m));
        }"""

if old_cat_match in app_js:
    app_js = app_js.replace(old_cat_match, new_cat_match)
    print("Updated multi-select card matching in applyFilters() successfully!")
else:
    print("WARNING: old_cat_match not found in app.js")

# D. Expose setCatalogFilterState and getCatalogFilterState in initProductsPage
old_reset_block = """    window.resetCatalogFilters = function () {
      activeCategory = 'all';
      activeMetal = 'all';
      activeFilter = 'all';
      maxPrice = 80000;
      activePriceRange = 'all';
      searchQuery = '';
      if (searchInput) searchInput.value = '';
      if (priceSlider) priceSlider.value = 80000;
      if (priceDisplay) priceDisplay.textContent = '₹80,000';
      highlightCategoryPills();
      highlightMetalButtons();
      highlightPricePills();
      applyFilters();
      applySort('featured');
    };"""

new_reset_block = """    window.setCatalogFilterState = function (newCats, newMetals) {
      if (Array.isArray(newCats) && newCats.length > 0) activeCategories = newCats;
      else if (newCats && typeof newCats === 'string') activeCategories = [newCats];
      else activeCategories = ['all'];
      activeCategory = activeCategories[0] || 'all';

      if (Array.isArray(newMetals) && newMetals.length > 0) activeMetals = newMetals;
      else if (newMetals && typeof newMetals === 'string') activeMetals = [newMetals];
      else activeMetals = ['all'];
      activeMetal = activeMetals[0] || 'all';

      highlightCategoryPills();
      highlightMetalButtons();
      applyFilters();

      try {
        const url = new URL(window.location.href);
        if (activeCategories.includes('all') || activeCategories.length === 0) {
          url.searchParams.delete('category');
        } else {
          url.searchParams.set('category', activeCategories.join(','));
        }
        if (activeMetals.includes('all') || activeMetals.length === 0) {
          url.searchParams.delete('metal');
        } else {
          url.searchParams.set('metal', activeMetals.join(','));
        }
        window.history.replaceState({}, '', url.toString());
      } catch (e) {}
    };

    window.getCatalogFilterState = function () {
      return {
        categories: [...activeCategories],
        metals: [...activeMetals]
      };
    };

    window.resetCatalogFilters = function () {
      activeCategories = ['all'];
      activeCategory = 'all';
      activeMetals = ['all'];
      activeMetal = 'all';
      activeFilter = 'all';
      maxPrice = 80000;
      activePriceRange = 'all';
      searchQuery = '';
      if (searchInput) searchInput.value = '';
      if (priceSlider) priceSlider.value = 80000;
      if (priceDisplay) priceDisplay.textContent = '₹80,000';
      highlightCategoryPills();
      highlightMetalButtons();
      highlightPricePills();
      applyFilters();
      applySort('featured');

      try {
        const url = new URL(window.location.href);
        url.searchParams.delete('category');
        url.searchParams.delete('metal');
        window.history.replaceState({}, '', url.toString());
      } catch (e) {}
    };"""

if old_reset_block in app_js:
    app_js = app_js.replace(old_reset_block, new_reset_block)
    print("Exposed setCatalogFilterState & getCatalogFilterState in app.js successfully!")
else:
    print("WARNING: old_reset_block not found in app.js")

# E. Rewrite openMobileFilterModal and interactive multi-select UI
modal_start = app_js.find("// Mobile Filter Drawer Modal for Catalog")
modal_end = app_js.find("// Size Guide Modal", modal_start)
if modal_start != -1 and modal_end != -1:
    new_modal_code = """// Mobile Filter Drawer Modal for Catalog (Interactive Multi-Select with In-Place Refresh)
  window._tempMobileCategories = new Set(['all']);
  window._tempMobileMetals = new Set(['all']);

  window.toggleMobileFilterCategory = function (cat) {
    if (cat === 'all') {
      window._tempMobileCategories.clear();
      window._tempMobileCategories.add('all');
    } else {
      window._tempMobileCategories.delete('all');
      if (window._tempMobileCategories.has(cat)) {
        window._tempMobileCategories.delete(cat);
        if (window._tempMobileCategories.size === 0) {
          window._tempMobileCategories.add('all');
        }
      } else {
        window._tempMobileCategories.add(cat);
      }
    }
    window._renderMobileFilterPillStates();
  };

  window.toggleMobileFilterMetal = function (metal) {
    if (metal === 'all') {
      window._tempMobileMetals.clear();
      window._tempMobileMetals.add('all');
    } else {
      window._tempMobileMetals.delete('all');
      if (window._tempMobileMetals.has(metal)) {
        window._tempMobileMetals.delete(metal);
        if (window._tempMobileMetals.size === 0) {
          window._tempMobileMetals.add('all');
        }
      } else {
        window._tempMobileMetals.add(metal);
      }
    }
    window._renderMobileFilterPillStates();
  };

  window._renderMobileFilterPillStates = function () {
    const catContainer = document.getElementById('mobile-filter-categories');
    if (catContainer) {
      const isAll = window._tempMobileCategories.has('all') || window._tempMobileCategories.size === 0;
      const catBtns = catContainer.querySelectorAll('button[data-filter-cat]');
      catBtns.forEach(btn => {
        const key = btn.getAttribute('data-filter-cat');
        const selected = (key === 'all') ? isAll : window._tempMobileCategories.has(key);
        if (selected) {
          btn.className = 'p-2.5 rounded-xl border border-[#61532E] bg-[#61532E] text-white font-semibold text-center transition-all duration-200 shadow-xs active:scale-95 cursor-pointer flex items-center justify-center gap-1.5';
        } else {
          btn.className = 'p-2.5 rounded-xl border border-stone-200 hover:border-[#61532E] bg-white text-stone-800 font-medium text-center transition-all duration-200 active:scale-95 cursor-pointer flex items-center justify-center gap-1.5';
        }
      });
    }

    const metalContainer = document.getElementById('mobile-filter-metals');
    if (metalContainer) {
      const isAllMetal = window._tempMobileMetals.has('all') || window._tempMobileMetals.size === 0;
      const metalBtns = metalContainer.querySelectorAll('button[data-filter-metal]');
      metalBtns.forEach(btn => {
        const key = btn.getAttribute('data-filter-metal');
        const selected = (key === 'all') ? isAllMetal : window._tempMobileMetals.has(key);
        if (selected) {
          btn.className = 'p-2.5 rounded-xl border border-[#61532E] bg-[#61532E] text-white font-semibold text-center transition-all duration-200 shadow-xs active:scale-95 cursor-pointer flex items-center justify-center gap-1.5';
        } else {
          btn.className = 'p-2.5 rounded-xl border border-stone-200 hover:border-[#61532E] bg-white text-stone-800 font-medium text-center transition-all duration-200 active:scale-95 cursor-pointer flex items-center justify-center gap-1.5';
        }
      });
    }
  };

  window.applyMobileFiltersAndClose = function () {
    const cats = Array.from(window._tempMobileCategories);
    const metals = Array.from(window._tempMobileMetals);
    if (window.setCatalogFilterState) {
      window.setCatalogFilterState(cats, metals);
    }
    window.closeMobileFilterModal();
    if (window.showToast) {
      window.showToast('Filters applied successfully');
    }
  };

  window.resetMobileFiltersAndClose = function () {
    window._tempMobileCategories = new Set(['all']);
    window._tempMobileMetals = new Set(['all']);
    if (window.resetCatalogFilters) {
      window.resetCatalogFilters();
    }
    window.closeMobileFilterModal();
  };

  window.openMobileFilterModal = function () {
    let m = document.getElementById('mobile-filter-modal');
    if (!m) {
      m = document.createElement('div');
      m.id = 'mobile-filter-modal';
      m.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-end sm:items-center justify-center font-sans';
      m.innerHTML = `
        <div class="bg-white w-full max-w-lg rounded-t-3xl sm:rounded-2xl p-6 pb-12 sm:pb-6 space-y-5 max-h-[85vh] overflow-y-auto no-scrollbar shadow-2xl border border-stone-200 animate-slide-up">
          <div class="flex items-center justify-between pb-3 border-b border-stone-200">
            <div>
              <h3 class="font-serif text-lg font-normal text-stone-900">Filter Atelier Creations</h3>
              <p class="text-[11px] text-stone-400 font-light mt-0.5">Select multiple categories &amp; finishes to filter in-place</p>
            </div>
            <button onclick="window.closeMobileFilterModal()" class="p-1.5 rounded-full hover:bg-stone-100 text-stone-400 hover:text-stone-800 transition-colors cursor-pointer" aria-label="Close filters">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="space-y-4 text-xs">
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
          </div>
          <div class="pt-4 grid grid-cols-2 gap-3 w-full border-t border-stone-100 mb-6 sm:mb-0">
            <button type="button" onclick="window.resetMobileFiltersAndClose()" class="w-full py-3 px-3 border border-stone-300 hover:border-stone-400 bg-white hover:bg-stone-50 rounded-xl text-xs font-semibold text-stone-700 active:scale-95 transition-all text-center flex items-center justify-center cursor-pointer shadow-xs">Reset Filters</button>
            <button type="button" onclick="window.applyMobileFiltersAndClose()" class="w-full py-3 px-3 bg-[#61532E] hover:bg-[#4A3F22] text-white rounded-xl text-xs font-bold uppercase tracking-wider active:scale-95 transition-all shadow-md text-center flex items-center justify-center cursor-pointer">Apply Filters</button>
          </div>
        </div>
      `;
      document.body.appendChild(m);
    }

    // Sync temporary state with current filter state
    const current = window.getCatalogFilterState ? window.getCatalogFilterState() : { categories: ['all'], metals: ['all'] };
    window._tempMobileCategories = new Set(current.categories);
    window._tempMobileMetals = new Set(current.metals);
    window._renderMobileFilterPillStates();

    m.classList.remove('hidden');
  };

  window.closeMobileFilterModal = function () {
    const m = document.getElementById('mobile-filter-modal');
    if (m) m.classList.add('hidden');
  };

  """
    app_js = app_js[:modal_start] + new_modal_code + app_js[modal_end:]
    print("Replaced openMobileFilterModal with modern multi-select implementation!")
else:
    print("WARNING: modal block markers not found in app.js")

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(app_js)
print("Updated jewellery-design-html/js/app.js successfully!")

print("\nAll code modifications in app.js completed.")


import os
import re

print("Starting implementation of smoothly animated Curated dropdown in filter modal & sidebar...")

# 1. Update app.js
with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update initProductsPage filter states to include activeCurated
old_state_init = """    // Filter states (supports single or multi-select array)
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

new_state_init = """    // Filter states (supports single or multi-select array)
    const params = new URLSearchParams(window.location.search);
    const rawCat = (params.get('category') || 'all').toLowerCase();
    let activeCategories = rawCat.split(',').map(s => s.trim()).filter(Boolean);
    if (activeCategories.length === 0) activeCategories = ['all'];
    let activeCategory = activeCategories[0] || 'all';

    const rawMetal = (params.get('metal') || 'all').toLowerCase();
    let activeMetals = rawMetal.split(',').map(s => s.trim()).filter(Boolean);
    if (activeMetals.length === 0) activeMetals = ['all'];
    let activeMetal = activeMetals[0] || 'all';

    const rawCurated = (params.get('curated') || '').toLowerCase();
    let activeCurated = rawCurated.split(',').map(s => s.trim()).filter(Boolean);

    let activeFilter = (params.get('filter') || 'all').toLowerCase();"""

if old_state_init in js:
    js = js.replace(old_state_init, new_state_init)
    print("Updated state init in app.js!")
else:
    print("WARNING: old_state_init not found")

# Update test single category and add curated matching
old_cat_helpers = """        // Helper for category matching
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

new_cat_helpers = """        // Helper for category matching
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

        // Helper for curated collection matching
        function testSingleCurated(curTarget) {
          if (curTarget === 'links_layers' || curTarget === 'links') {
            return cat === 'necklaces' || name.includes('chain') || name.includes('link') || name.includes('layer') || name.includes('choker') || name.includes('lariat');
          }
          if (curTarget === 'drops_halo' || curTarget === 'halo') {
            return name.includes('halo') || name.includes('drop') || name.includes('cocktail') || name.includes('stud') || cat === 'earrings';
          }
          if (curTarget === 'dainty_steps' || curTarget === 'anklets') {
            return cat === 'anklets' || name.includes('anklet') || name.includes('charm') || name.includes('payal');
          }
          if (curTarget === 'daily_luxe' || curTarget === 'gold') {
            return metal === 'gold' || name.includes('gold') || name.includes('vermeil');
          }
          if (curTarget === 'tennis_fever' || curTarget === 'tennis') {
            return name.includes('tennis') || (cat === 'bracelets' && (name.includes('bracelet') || name.includes('cuff')));
          }
          if (curTarget === 'heirloom_suites' || curTarget === 'suites' || curTarget === 'sets') {
            return cat === 'complete_sets' || cat === 'sets' || name.includes('set') || name.includes('suite') || name.includes('gift');
          }
          return true;
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
        }

        // Multi-select Curated match
        let curatedMatch = false;
        if (activeCurated.length === 0 || activeCurated.includes('all')) {
          curatedMatch = true;
        } else {
          curatedMatch = activeCurated.some(cur => testSingleCurated(cur));
        }"""

if old_cat_helpers in js:
    js = js.replace(old_cat_helpers, new_cat_helpers)
    print("Updated card match helpers to support curated matching!")
else:
    print("WARNING: old_cat_helpers not found")

# Update card display condition to include curatedMatch
old_display_check = "const isVisible = catMatch && metalMatch && filterMatch && priceMatch && searchMatch;"
new_display_check = "const isVisible = catMatch && metalMatch && curatedMatch && filterMatch && priceMatch && searchMatch;"

if old_display_check in js:
    js = js.replace(old_display_check, new_display_check)
    print("Updated isVisible condition with curatedMatch!")

# Update setCatalogFilterState and getCatalogFilterState
old_set_filter = """    window.setCatalogFilterState = function (newCats, newMetals) {
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
    };"""

new_set_filter = """    window.setCatalogFilterState = function (newCats, newMetals, newCurated) {
      if (Array.isArray(newCats) && newCats.length > 0) activeCategories = newCats;
      else if (newCats && typeof newCats === 'string') activeCategories = [newCats];
      else activeCategories = ['all'];
      activeCategory = activeCategories[0] || 'all';

      if (Array.isArray(newMetals) && newMetals.length > 0) activeMetals = newMetals;
      else if (newMetals && typeof newMetals === 'string') activeMetals = [newMetals];
      else activeMetals = ['all'];
      activeMetal = activeMetals[0] || 'all';

      if (Array.isArray(newCurated)) activeCurated = newCurated;
      else if (newCurated && typeof newCurated === 'string') activeCurated = [newCurated];
      else activeCurated = [];

      highlightCategoryPills();
      highlightMetalButtons();
      highlightSidebarCurated();
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
        if (activeCurated.length === 0) {
          url.searchParams.delete('curated');
        } else {
          url.searchParams.set('curated', activeCurated.join(','));
        }
        window.history.replaceState({}, '', url.toString());
      } catch (e) {}
    };

    window.getCatalogFilterState = function () {
      return {
        categories: [...activeCategories],
        metals: [...activeMetals],
        curated: [...activeCurated]
      };
    };

    function highlightSidebarCurated() {
      const curBtns = document.querySelectorAll('[data-curated-filter]');
      curBtns.forEach(btn => {
        const key = btn.getAttribute('data-curated-filter');
        const isMatch = activeCurated.includes(key);
        if (isMatch) {
          btn.className = 'w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer bg-[#61532E]/10 text-[#61532E] font-semibold';
        } else {
          btn.className = 'w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50';
        }
      });
    }

    window.toggleSidebarCurated = function (key) {
      if (activeCurated.includes(key)) {
        activeCurated = activeCurated.filter(k => k !== key);
      } else {
        activeCurated.push(key);
      }
      highlightSidebarCurated();
      applyFilters();
    };"""

if old_set_filter in js:
    js = js.replace(old_set_filter, new_set_filter)
    print("Updated setCatalogFilterState to accept curated collections!")
else:
    print("WARNING: old_set_filter not found")

# Rewrite mobile filter modal to include the Curated Collections collapsible animated dropdown
modal_marker = "// Mobile Filter Drawer Modal for Catalog (Interactive Multi-Select with In-Place Refresh)"
modal_end_marker = "// Size Guide Modal"

start_idx = js.find(modal_marker)
end_idx = js.find(modal_end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_full_modal = """// Mobile Filter Drawer Modal for Catalog (Interactive Multi-Select with In-Place Refresh & Curated Dropdown)
  window._tempMobileCategories = new Set(['all']);
  window._tempMobileMetals = new Set(['all']);
  window._tempMobileCurated = new Set();

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

  window.toggleMobileFilterCurated = function (curKey) {
    if (window._tempMobileCurated.has(curKey)) {
      window._tempMobileCurated.delete(curKey);
    } else {
      window._tempMobileCurated.add(curKey);
    }
    window._renderMobileFilterPillStates();
  };

  window.toggleModalCuratedDropdown = function () {
    const container = document.getElementById('modal-curated-container');
    const chevron = document.getElementById('chevron-modal-curated');
    if (!container) return;

    const isHidden = container.classList.contains('hidden');
    if (isHidden) {
      container.classList.remove('hidden');
      container.style.maxHeight = '0px';
      container.style.opacity = '0';
      void container.offsetHeight; // force repaint
      container.style.transition = 'max-height 0.35s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.3s ease';
      container.style.maxHeight = (container.scrollHeight + 15) + 'px';
      container.style.opacity = '1';
      if (chevron) {
        chevron.style.transition = 'transform 0.35s cubic-bezier(0.22, 1, 0.36, 1)';
        chevron.classList.add('rotate-180', 'text-[#61532E]');
      }
      setTimeout(function () { container.style.maxHeight = 'none'; }, 350);
    } else {
      container.style.maxHeight = container.scrollHeight + 'px';
      container.style.opacity = '1';
      void container.offsetHeight;
      container.style.transition = 'max-height 0.35s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.3s ease';
      container.style.maxHeight = '0px';
      container.style.opacity = '0';
      if (chevron) {
        chevron.style.transition = 'transform 0.35s cubic-bezier(0.22, 1, 0.36, 1)';
        chevron.classList.remove('rotate-180', 'text-[#61532E]');
      }
      setTimeout(function () { container.classList.add('hidden'); container.style.maxHeight = ''; }, 350);
    }
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

    const curatedContainer = document.getElementById('mobile-filter-curated');
    if (curatedContainer) {
      const curBtns = curatedContainer.querySelectorAll('button[data-filter-curated]');
      curBtns.forEach(btn => {
        const key = btn.getAttribute('data-filter-curated');
        const selected = window._tempMobileCurated.has(key);
        if (selected) {
          btn.className = 'p-2 rounded-xl border border-[#61532E] bg-[#61532E] text-white font-semibold text-center transition-all duration-200 shadow-xs active:scale-95 cursor-pointer flex items-center justify-center gap-1';
        } else {
          btn.className = 'p-2 rounded-xl border border-stone-200 hover:border-[#61532E] bg-[#FAF8F5] text-stone-800 font-medium text-center transition-all duration-200 active:scale-95 cursor-pointer flex items-center justify-center gap-1';
        }
      });

      const summary = document.getElementById('modal-curated-summary');
      if (summary) {
        summary.textContent = window._tempMobileCurated.size > 0 ? `${window._tempMobileCurated.size} selected` : 'Explore';
      }
    }
  };

  window.applyMobileFiltersAndClose = function () {
    const cats = Array.from(window._tempMobileCategories);
    const metals = Array.from(window._tempMobileMetals);
    const curated = Array.from(window._tempMobileCurated);
    if (window.setCatalogFilterState) {
      window.setCatalogFilterState(cats, metals, curated);
    }
    window.closeMobileFilterModal();
    if (window.showToast) {
      window.showToast('Filters applied successfully');
    }
  };

  window.resetMobileFiltersAndClose = function () {
    window._tempMobileCategories = new Set(['all']);
    window._tempMobileMetals = new Set(['all']);
    window._tempMobileCurated = new Set();
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
        <div class="bg-white w-full max-w-lg rounded-t-3xl sm:rounded-2xl p-6 pb-14 sm:pb-6 space-y-4 max-h-[88vh] overflow-y-auto no-scrollbar shadow-2xl border border-stone-200 animate-slide-up">
          <div class="flex items-center justify-between pb-3 border-b border-stone-200">
            <div>
              <h3 class="font-serif text-lg font-normal text-stone-900">Filter Atelier Creations</h3>
              <p class="text-[11px] text-stone-400 font-light mt-0.5">Select multiple categories, finishes &amp; curated collections</p>
            </div>
            <button onclick="window.closeMobileFilterModal()" class="p-1.5 rounded-full hover:bg-stone-100 text-stone-400 hover:text-stone-800 transition-colors cursor-pointer" aria-label="Close filters">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="space-y-4 text-xs">
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

            <!-- 3. Curated Collections Accordion (Collapsible with smooth animation) -->
            <div class="rounded-xl border border-[#CEBDA7]/70 bg-[#FAF8F5]/80 overflow-hidden shadow-2xs">
              <button type="button" onclick="window.toggleModalCuratedDropdown()" class="w-full flex items-center justify-between p-3 text-left cursor-pointer active:bg-[#F6F3EE] transition-colors" aria-expanded="false">
                <div class="flex items-center gap-2">
                  <span class="w-3.5 h-3.5 rounded-full border border-white shrink-0 shadow-xs" style="background: linear-gradient(135deg, #F3E8D6 0%, #C5A059 50%, #61532E 100%);"></span>
                  <div>
                    <div class="font-bold text-stone-900 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                      <span>Curated Collections</span>
                      <span class="text-[8px] px-1 py-0.2 rounded bg-white text-[#61532E] border border-[#CEBDA7]/80 font-bold uppercase">Dropdown</span>
                    </div>
                    <div class="text-[9.5px] text-stone-400 font-light">Tap to expand curated suites &amp; links</div>
                  </div>
                </div>
                <div class="flex items-center gap-1.5">
                  <span class="text-[10px] text-[#61532E] font-medium" id="modal-curated-summary">Explore</span>
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

          <!-- Bottom Action Buttons with ample breathing space -->
          <div class="pt-4 grid grid-cols-2 gap-3 w-full border-t border-stone-100 mb-6 sm:mb-0">
            <button type="button" onclick="window.resetMobileFiltersAndClose()" class="w-full py-3 px-3 border border-stone-300 hover:border-stone-400 bg-white hover:bg-stone-50 rounded-xl text-xs font-semibold text-stone-700 active:scale-95 transition-all text-center flex items-center justify-center cursor-pointer shadow-xs">Reset Filters</button>
            <button type="button" onclick="window.applyMobileFiltersAndClose()" class="w-full py-3 px-3 bg-[#61532E] hover:bg-[#4A3F22] text-white rounded-xl text-xs font-bold uppercase tracking-wider active:scale-95 transition-all shadow-md text-center flex items-center justify-center cursor-pointer">Apply Filters</button>
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

    m.classList.remove('hidden');
  };

  window.closeMobileFilterModal = function () {
    const m = document.getElementById('mobile-filter-modal');
    if (m) m.classList.add('hidden');
  };

  """
    js = js[:start_idx] + new_full_modal + js[end_idx:]
    print("Replaced openMobileFilterModal with Curated Dropdown included!")
else:
    print("WARNING: modal markers not found")

with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js successfully!")

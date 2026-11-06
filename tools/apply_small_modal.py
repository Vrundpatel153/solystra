with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('window.openMobileFilterModal = function () {')
end = text.find('// Size Guide Modal', start)

new_filter_code = """window.openMobileFilterModal = function () {
    let m = document.getElementById('mobile-filter-modal');
    if (!m) {
      m = document.createElement('div');
      m.id = 'mobile-filter-modal';
      m.style.cssText = 'position:fixed; inset:0; z-index:999999; background:rgba(0,0,0,0.65); backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); display:flex; align-items:center; justify-content:center; padding:16px; box-sizing:border-box; font-family:"Plus Jakarta Sans",system-ui,sans-serif;';
      m.onclick = function (e) {
        if (e.target === m) {
          window.closeMobileFilterModal();
        }
      };
      m.innerHTML = `
        <div style="background:#ffffff; width:100%; max-width:380px; height:480px; max-height:calc(100vh - 32px); max-height:calc(100dvh - 32px); border-radius:16px; border:1px solid #CEBDA7; box-shadow:0 20px 45px rgba(0,0,0,0.35); display:flex; flex-direction:column; overflow:hidden; margin:auto; box-sizing:border-box;">
          
          <!-- 1. COMPACT PINNED HEADER -->
          <div style="flex-shrink:0; height:46px; padding:0 16px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #EAE4DC; background:#FAF8F5; user-select:none; box-sizing:border-box;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="font-family:'Fraunces',serif; font-size:16px; font-weight:600; color:#1C1917;">Filters</span>
              <span id="modal-active-count-badge" style="font-size:10px; background:#61532E; color:#FFFFFF; padding:1px 7px; border-radius:10px; font-weight:600; display:none;">0</span>
            </div>
            <button type="button" onclick="window.closeMobileFilterModal()" style="width:28px; height:28px; border-radius:50%; border:1px solid #CEBDA7; background:#ffffff; display:flex; align-items:center; justify-content:center; color:#44403C; cursor:pointer; transition:all 0.15s; padding:0;" aria-label="Close">
              <svg style="width:14px; height:14px;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- 2. SCROLLABLE MIDDLE BODY WITH THIN SCROLLER -->
          <div id="filter-modal-scroll" style="flex:1 1 auto; min-height:0; overflow-y:auto; -webkit-overflow-scrolling:touch; padding:14px 16px; display:flex; flex-direction:column; gap:14px; scrollbar-width:thin; scrollbar-color:#C5A059 transparent; box-sizing:border-box; background:#ffffff;">
            
            <!-- A. Max Budget Slider -->
            <div style="background:#FAF8F5; border:1px solid #EAE4DC; border-radius:10px; padding:10px 12px; box-sizing:border-box;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#44403C;">Max Budget</span>
                <span id="modal-budget-display" style="font-size:12px; font-weight:700; color:#61532E;">₹80,000</span>
              </div>
              <input type="range" id="modal-budget-slider" min="1000" max="80000" step="1000" value="80000" oninput="window.setModalMaxPrice(this.value)" style="width:100%; accent-color:#61532E; cursor:pointer; margin:2px 0; height:4px; display:block;" />
              <div style="display:flex; justify-content:space-between; font-size:9px; color:#78716C; margin-top:2px;">
                <span>₹1,000</span>
                <span>₹80,000+</span>
              </div>
            </div>

            <!-- B. Category (2-Col Grid) -->
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#44403C;">Category</span>
                <span style="font-size:9.5px; color:#A8A29E;">Multi-select</span>
              </div>
              <div id="mobile-filter-categories" style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                <button type="button" data-filter-cat="all" onclick="window.toggleMobileFilterCategory('all')">All Creations</button>
                <button type="button" data-filter-cat="bracelets" onclick="window.toggleMobileFilterCategory('bracelets')">Bracelets &amp; Kadas</button>
                <button type="button" data-filter-cat="necklaces" onclick="window.toggleMobileFilterCategory('necklaces')">Necklaces &amp; Pendants</button>
                <button type="button" data-filter-cat="rings" onclick="window.toggleMobileFilterCategory('rings')">Rings &amp; Bands</button>
                <button type="button" data-filter-cat="earrings" onclick="window.toggleMobileFilterCategory('earrings')">Earrings &amp; Studs</button>
                <button type="button" data-filter-cat="complete_sets" onclick="window.toggleMobileFilterCategory('complete_sets')">Gift Sets &amp; Suites</button>
                <button type="button" data-filter-cat="chains" onclick="window.toggleMobileFilterCategory('chains')">Layering Chains</button>
                <button type="button" data-filter-cat="anklets" onclick="window.toggleMobileFilterCategory('anklets')">Silver Anklets</button>
              </div>
            </div>

            <!-- C. Precious Finish (2-Col Grid) -->
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#44403C;">Precious Finish</span>
                <span style="font-size:9.5px; color:#A8A29E;">Multi-select</span>
              </div>
              <div id="mobile-filter-metals" style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                <button type="button" data-filter-metal="all" onclick="window.toggleMobileFilterMetal('all')">All Finishes</button>
                <button type="button" data-filter-metal="silver" onclick="window.toggleMobileFilterMetal('silver')">Pure 925 Silver</button>
                <button type="button" data-filter-metal="gold" onclick="window.toggleMobileFilterMetal('gold')">18K Gold Vermeil</button>
                <button type="button" data-filter-metal="rose" onclick="window.toggleMobileFilterMetal('rose')">18K Rose Gold</button>
              </div>
            </div>

            <!-- D. Curated Collections (2-Col Grid) -->
            <div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#44403C;">Curated Collections</span>
                <span style="font-size:9.5px; color:#A8A29E;">Multi-select</span>
              </div>
              <div id="mobile-filter-curated" style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                <button type="button" data-filter-curated="links_layers" onclick="window.toggleMobileFilterCurated('links_layers')">Links &amp; Layers</button>
                <button type="button" data-filter-curated="drops_halo" onclick="window.toggleMobileFilterCurated('drops_halo')">Drops &amp; Halo</button>
                <button type="button" data-filter-curated="dainty_steps" onclick="window.toggleMobileFilterCurated('dainty_steps')">Dainty Steps</button>
                <button type="button" data-filter-curated="daily_luxe" onclick="window.toggleMobileFilterCurated('daily_luxe')">Daily Luxe</button>
                <button type="button" data-filter-curated="tennis_fever" onclick="window.toggleMobileFilterCurated('tennis_fever')">Tennis Fever</button>
                <button type="button" data-filter-curated="heirloom_suites" onclick="window.toggleMobileFilterCurated('heirloom_suites')">Heirloom Suites</button>
              </div>
            </div>

          </div>

          <!-- 3. COMPACT PINNED FOOTER -->
          <div style="flex-shrink:0; height:48px; padding:7px 16px; border-top:1px solid #EAE4DC; background:#FAF8F5; display:grid; grid-template-columns:1fr 1.3fr; gap:8px; box-sizing:border-box;">
            <button type="button" onclick="window.resetMobileFiltersAndClose()" style="height:34px; border-radius:8px; border:1px solid #CEBDA7; background:#ffffff; font-size:11.5px; font-weight:600; color:#57534E; cursor:pointer; transition:all 0.15s; padding:0;">Reset</button>
            <button type="button" onclick="window.applyMobileFiltersAndClose()" style="height:34px; border-radius:8px; border:none; background:#61532E; font-size:11.5px; font-weight:600; color:#ffffff; cursor:pointer; transition:all 0.15s; padding:0; letter-spacing:0.02em;">Apply Filters</button>
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

    m.style.display = 'flex';
  };

  window.closeMobileFilterModal = function () {
    const m = document.getElementById('mobile-filter-modal');
    if (m) m.style.display = 'none';
    document.body.style.overflow = '';
    if (window._filterModalEscHandler) {
      window.removeEventListener('keydown', window._filterModalEscHandler);
    }
  };

  window.openFilterModal = window.openMobileFilterModal;
  window.closeFilterModal = window.closeMobileFilterModal;

  window._modalMaxPrice = 80000;
  window.setModalMaxPrice = function (val) {
    window._modalMaxPrice = Number(val);
    const disp = document.getElementById('modal-budget-display');
    if (disp) {
      disp.innerText = '₹' + Number(val).toLocaleString('en-IN');
    }
  };

  window.toggleMobileFilterCategory = function (cat) {
    if (cat === 'all') {
      window._tempMobileCategories = new Set(['all']);
    } else {
      window._tempMobileCategories.delete('all');
      if (window._tempMobileCategories.has(cat)) {
        window._tempMobileCategories.delete(cat);
        if (window._tempMobileCategories.size === 0) window._tempMobileCategories.add('all');
      } else {
        window._tempMobileCategories.add(cat);
      }
    }
    window._renderMobileFilterPillStates();
  };

  window.toggleMobileFilterMetal = function (metal) {
    if (metal === 'all') {
      window._tempMobileMetals = new Set(['all']);
    } else {
      window._tempMobileMetals.delete('all');
      if (window._tempMobileMetals.has(metal)) {
        window._tempMobileMetals.delete(metal);
        if (window._tempMobileMetals.size === 0) window._tempMobileMetals.add('all');
      } else {
        window._tempMobileMetals.add(metal);
      }
    }
    window._renderMobileFilterPillStates();
  };

  window.toggleMobileFilterCurated = function (curatedKey) {
    if (window._tempMobileCurated.has(curatedKey)) {
      window._tempMobileCurated.delete(curatedKey);
    } else {
      window._tempMobileCurated.add(curatedKey);
    }
    window._renderMobileFilterPillStates();
  };

  window._renderMobileFilterPillStates = function () {
    const activeStyle = 'height:30px; border-radius:6px; font-size:11px; font-weight:600; background:#61532E; color:#ffffff; border:1px solid #61532E; cursor:pointer; transition:all 0.15s; padding:0 8px; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; display:flex; align-items:center; justify-content:center; box-sizing:border-box;';
    const inactiveStyle = 'height:30px; border-radius:6px; font-size:11px; font-weight:500; background:#FAF8F5; color:#44403C; border:1px solid #EAE4DC; cursor:pointer; transition:all 0.15s; padding:0 8px; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; display:flex; align-items:center; justify-content:center; box-sizing:border-box;';

    // Categories
    document.querySelectorAll('#mobile-filter-categories button').forEach(btn => {
      const c = btn.getAttribute('data-filter-cat');
      btn.style.cssText = window._tempMobileCategories.has(c) ? activeStyle : inactiveStyle;
    });

    // Metals
    document.querySelectorAll('#mobile-filter-metals button').forEach(btn => {
      const m = btn.getAttribute('data-filter-metal');
      btn.style.cssText = window._tempMobileMetals.has(m) ? activeStyle : inactiveStyle;
    });

    // Curated
    document.querySelectorAll('#mobile-filter-curated button').forEach(btn => {
      const k = btn.getAttribute('data-filter-curated');
      btn.style.cssText = window._tempMobileCurated.has(k) ? activeStyle : inactiveStyle;
    });

    // Badge count
    let count = 0;
    if (!window._tempMobileCategories.has('all')) count += window._tempMobileCategories.size;
    if (!window._tempMobileMetals.has('all')) count += window._tempMobileMetals.size;
    count += window._tempMobileCurated.size;
    const badge = document.getElementById('modal-active-count-badge');
    if (badge) {
      if (count > 0) {
        badge.innerText = count;
        badge.style.display = 'inline-block';
      } else {
        badge.style.display = 'none';
      }
    }
  };

  window.resetMobileFiltersAndClose = function () {
    window._tempMobileCategories = new Set(['all']);
    window._tempMobileMetals = new Set(['all']);
    window._tempMobileCurated = new Set();
    window._modalMaxPrice = 80000;
    const slider = document.getElementById('modal-budget-slider');
    if (slider) slider.value = 80000;
    const disp = document.getElementById('modal-budget-display');
    if (disp) disp.innerText = '₹80,000';
    window._renderMobileFilterPillStates();
    if (window.resetCatalogFilters) {
      window.resetCatalogFilters();
    }
    window.closeMobileFilterModal();
  };

  window.applyMobileFiltersAndClose = function () {
    if (window.setCatalogFilterState) {
      window.setCatalogFilterState({
        categories: Array.from(window._tempMobileCategories),
        metals: Array.from(window._tempMobileMetals),
        curated: Array.from(window._tempMobileCurated),
        maxPrice: window._modalMaxPrice || 80000
      });
    }
    window.closeMobileFilterModal();
  };
"""

new_text = text[:start] + new_filter_code + text[end:]
with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Applied ultra-compact, simple small centered modal to app.js!")

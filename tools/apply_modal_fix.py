with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_func_start = text.find('window.openMobileFilterModal = function () {')
assert old_func_start != -1, "Could not find window.openMobileFilterModal"

old_func_end = text.find('// Size Guide Modal', old_func_start)
assert old_func_end != -1, "Could not find Size Guide Modal"

new_func = """window.openMobileFilterModal = function () {
    let m = document.getElementById('mobile-filter-modal');
    if (!m) {
      m = document.createElement('div');
      m.id = 'mobile-filter-modal';
      m.style.cssText = 'position:fixed; inset:0; z-index:99999; background:rgba(20,16,10,0.75); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); display:flex; align-items:center; justify-content:center; padding:0.75rem; font-family:sans-serif; overflow:hidden;';
      m.onclick = function (e) {
        if (e.target === m) {
          window.closeMobileFilterModal();
        }
      };
      m.innerHTML = `
        <div style="background:#ffffff; width:100%; max-width:32rem; max-height:calc(100vh - 1.5rem); max-height:calc(100dvh - 1.5rem); display:flex; flex-direction:column; border-radius:1.25rem; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0,0,0,0.4); border:1px solid rgba(206,189,167,0.8); margin:auto;">
          
          <!-- 1. STICKY TOP HEADER (Always 100% visible, never scrolls out of view) -->
          <div style="flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:1rem 1.25rem; border-bottom:1px solid rgba(206,189,167,0.6); background:#FAF8F5; user-select:none;">
            <div style="display:flex; align-items:center; gap:0.625rem; min-width:0;">
              <div style="width:2rem; height:2rem; border-radius:9999px; background:rgba(97,83,46,0.1); display:flex; align-items:center; justify-content:center; color:#61532E; flex-shrink:0;">
                <svg style="width:1rem; height:1rem;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="21" x2="14" y1="4" y2="4"></line><line x1="10" x2="3" y1="4" y2="4"></line><line x1="21" x2="12" y1="12" y2="12"></line><line x1="8" x2="3" y1="12" y2="12"></line><line x1="21" x2="16" y1="20" y2="20"></line><line x1="12" x2="3" y1="20" y2="20"></line><line x1="14" x2="14" y1="2" y2="6"></line><line x1="8" x2="8" y1="10" y2="14"></line><line x1="16" x2="16" y1="18" y2="22"></line></svg>
              </div>
              <div style="min-width:0;">
                <h3 style="font-family:serif; font-size:1.125rem; font-weight:600; color:#1c1917; line-height:1.2; margin:0;">Filter Atelier Creations</h3>
                <p style="font-size:0.6875rem; color:#78716c; margin:0.25rem 0 0 0; font-weight:300;">Customise budget, categories, metals &amp; collections</p>
              </div>
            </div>
            <button type="button" onclick="window.closeMobileFilterModal()" style="width:2.25rem; height:2.25rem; border-radius:9999px; background:#ffffff; border:1px solid #CEBDA7; display:flex; align-items:center; justify-content:center; color:#44403c; cursor:pointer; flex-shrink:0; margin-left:0.5rem; transition:all 0.2s;" aria-label="Close filters">
              <svg style="width:1.25rem; height:1.25rem;" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>

          <!-- 2. SCROLLABLE MIDDLE BODY (min-height:0 enables shrink; smooth scroll with visible scrollbar) -->
          <div class="flex-1" style="flex:1 1 auto; min-height:0; overflow-y:auto; -webkit-overflow-scrolling:touch; padding:1.25rem; display:flex; flex-direction:column; gap:1.25rem; font-size:0.75rem; background:#ffffff; scrollbar-width:thin; scrollbar-color:#CEBDA7 #FAF8F5;">
            
            <!-- 0. Max Budget Slider -->
            <div style="border-radius:0.75rem; border:1px solid rgba(206,189,167,0.7); background:rgba(250,248,245,0.9); padding:0.875rem; display:flex; flex-direction:column; gap:0.5rem;">
              <div style="display:flex; align-items:center; justify-content:space-between;">
                <span style="font-weight:700; color:#292524; text-transform:uppercase; letter-spacing:0.05em; font-size:0.6875rem;">Max Budget</span>
                <span id="modal-budget-display" style="font-weight:700; font-size:0.75rem; color:#61532E;">₹80,000</span>
              </div>
              <input type="range" id="modal-budget-slider" min="1000" max="80000" step="1000" value="80000" oninput="window.setModalMaxPrice(this.value)" style="width:100%; accent-color:#61532E; cursor:pointer;" />
              <div style="display:flex; align-items:center; justify-content:space-between; font-size:0.625rem; color:#a8a29e; font-weight:300;">
                <span>₹1,000</span>
                <span>₹80,000+</span>
              </div>
            </div>

            <!-- 1. Category -->
            <div>
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.5rem;">
                <span style="font-weight:700; color:#292524; text-transform:uppercase; letter-spacing:0.05em;">Category</span>
                <span style="font-size:0.625rem; color:#a8a29e;">Multi-selectable</span>
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
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.5rem;">
                <span style="font-weight:700; color:#292524; text-transform:uppercase; letter-spacing:0.05em;">Precious Finish</span>
                <span style="font-size:0.625rem; color:#a8a29e;">Multi-selectable</span>
              </div>
              <div class="grid grid-cols-2 gap-2" id="mobile-filter-metals">
                <button type="button" data-filter-metal="all" onclick="window.toggleMobileFilterMetal('all')">All Finishes</button>
                <button type="button" data-filter-metal="silver" onclick="window.toggleMobileFilterMetal('silver')">Pure 925 Silver</button>
                <button type="button" data-filter-metal="gold" onclick="window.toggleMobileFilterMetal('gold')">18K Gold Vermeil</button>
                <button type="button" data-filter-metal="rose" onclick="window.toggleMobileFilterMetal('rose')">18K Rose Gold</button>
              </div>
            </div>

            <!-- 3. Curated Collections Accordion -->
            <div style="border-radius:0.75rem; border:1px solid rgba(206,189,167,0.7); background:rgba(250,248,245,0.9); overflow:hidden;">
              <button type="button" onclick="window.toggleModalCuratedDropdown()" style="width:100%; display:flex; align-items:center; justify-content:space-between; padding:0.75rem; text-align:left; cursor:pointer; background:transparent; border:none; transition:background 0.2s;" aria-expanded="false">
                <div style="display:flex; align-items:center; gap:0.625rem;">
                  <span style="width:0.875rem; height:0.875rem; border-radius:9999px; border:1px solid #ffffff; flex-shrink:0; background:linear-gradient(135deg, #F3E8D6 0%, #C5A059 50%, #61532E 100%);"></span>
                  <div>
                    <span style="font-weight:700; color:#1c1917; text-transform:uppercase; letter-spacing:0.05em; font-size:0.6875rem; display:block;">Curated Collections</span>
                    <span style="font-size:0.59375rem; color:#a8a29e; font-weight:300; display:block; margin-top:0.125rem;">Tap to expand curated suites &amp; links</span>
                  </div>
                </div>
                <div style="display:flex; align-items:center; gap:0.375rem;">
                  <span class="hidden" id="modal-curated-summary"></span>
                  <svg style="width:1rem; height:1rem; color:#78716c; transition:transform 0.3s;" id="chevron-modal-curated" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"></path></svg>
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

          <!-- 3. STICKY BOTTOM FOOTER (Always 100% visible, never scrolls out of view) -->
          <div style="flex-shrink:0; padding:0.875rem 1.25rem; border-top:1px solid rgba(206,189,167,0.6); background:#FAF8F5; display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; user-select:none; box-shadow:0 -4px 16px rgba(0,0,0,0.03);">
            <button type="button" onclick="window.resetMobileFiltersAndClose()" style="width:100%; padding:0.625rem 0.75rem; border:1px solid #CEBDA7; background:#ffffff; border-radius:0.75rem; font-size:0.75rem; font-weight:600; color:#44403c; cursor:pointer; transition:all 0.15s; text-align:center;">Reset Filters</button>
            <button type="button" onclick="window.applyMobileFiltersAndClose()" style="width:100%; padding:0.625rem 0.75rem; background:#61532E; color:#ffffff; border:none; border-radius:0.75rem; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; cursor:pointer; transition:all 0.15s; text-align:center; box-shadow:0 2px 8px rgba(97,83,46,0.3);">Apply Filters</button>
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

  """

text = text[:old_func_start] + new_func + text[old_func_end:]

with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Applied 100% fail-safe inline style 3-tier modal architecture to app.js!")

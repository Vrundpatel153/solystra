import re

def update_catalog_engine():
    js_path = 'jewellery-design-html/js/app.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    # 1. Update window.openFilterModal alias and enhance openMobileFilterModal with max budget slider
    # Let's inspect window.openMobileFilterModal in app.js
    old_modal_start = js.find('window.openMobileFilterModal = function () {')
    if old_modal_start == -1:
        print("ERROR: could not find window.openMobileFilterModal definition")
        return

    # Let's find where the modal template is inside openMobileFilterModal
    # We want to insert the Max Budget section right before Category or before Curated
    budget_slider_html = """
            <!-- 0. Max Budget Slider -->
            <div class="rounded-xl border border-[#CEBDA7]/70 bg-[#FAF8F5]/80 p-3.5 shadow-2xs space-y-2 mb-3">
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
"""

    # Check if budget slider already in modal
    if 'id="modal-budget-slider"' not in js:
        cat_pos = js.find('<!-- 1. Category -->', old_modal_start)
        if cat_pos != -1:
            js = js[:cat_pos] + budget_slider_html + js[cat_pos:]
            print("Inserted budget slider into filter modal.")

    # 2. Add helper window.setModalMaxPrice and window.openFilterModal
    helpers_code = """
  // Global filter modal open aliases
  window.openFilterModal = function () {
    if (window.openMobileFilterModal) window.openMobileFilterModal();
  };
  window.closeFilterModal = function () {
    if (window.closeMobileFilterModal) window.closeMobileFilterModal();
  };
  window._modalMaxPrice = 80000;
  window.setModalMaxPrice = function (val) {
    window._modalMaxPrice = parseInt(val, 10);
    const disp = document.getElementById('modal-budget-display');
    if (disp) disp.textContent = '₹' + window._modalMaxPrice.toLocaleString('en-IN');
  };
"""

    if 'window.openFilterModal =' not in js:
        # insert right before window.openMobileFilterModal
        pos_open_fn = js.find('window.openMobileFilterModal = function')
        js = js[:pos_open_fn] + helpers_code + '\n' + js[pos_open_fn:]
        print("Added window.openFilterModal alias and setModalMaxPrice.")

    # 3. Enhance applyMobileFiltersAndClose to also pass max price
    old_apply_fn = js.find('window.applyMobileFiltersAndClose = function () {')
    if old_apply_fn != -1:
        # find where window.setCatalogFilterState is called
        call_pos = js.find('window.setCatalogFilterState(', old_apply_fn)
        if call_pos != -1 and 'window.setCatalogMaxPrice' not in js[old_apply_fn:old_apply_fn+1000]:
            # Insert window.setCatalogMaxPrice before or after
            call_end = js.find(');', call_pos) + 2
            insertion = "\n    if (window.setCatalogMaxPrice && window._modalMaxPrice) window.setCatalogMaxPrice(window._modalMaxPrice);"
            js = js[:call_end] + insertion + js[call_end:]
            print("Updated applyMobileFiltersAndClose with max price sync.")

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Filter modal helpers updated.")

if __name__ == '__main__':
    update_catalog_engine()


import os

with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

sidebar_toggle_fn = """  window.toggleSidebarCuratedDropdown = function () {
    const container = document.getElementById('sidebar-curated-container');
    const chevron = document.getElementById('chevron-sidebar-curated');
    if (!container) return;
    const isHidden = container.classList.contains('hidden');
    if (isHidden) {
      container.classList.remove('hidden');
      container.style.maxHeight = '0px';
      container.style.opacity = '0';
      void container.offsetHeight;
      container.style.transition = 'max-height 0.35s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.3s ease';
      container.style.maxHeight = (container.scrollHeight + 10) + 'px';
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
"""

if "window.toggleSidebarCuratedDropdown" not in js:
    pos = js.find("window.toggleModalCuratedDropdown")
    js = js[:pos] + sidebar_toggle_fn + "\n" + js[pos:]
    with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Added toggleSidebarCuratedDropdown to app.js!")

# Update products.html sidebar
with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    p_html = f.read()

curated_sidebar_snippet = """<div class="pt-4 border-t border-[#CEBDA7]">
  <button type="button" onclick="window.toggleSidebarCuratedDropdown()" class="w-full flex items-center justify-between text-left py-1 cursor-pointer group">
    <div class="flex items-center gap-2">
      <span class="text-xs font-bold uppercase tracking-wider text-stone-800">Curated Collections</span>
      <span class="text-[9px] px-1.5 py-0.5 rounded-full bg-[#61532E]/10 text-[#61532E] font-semibold">Dropdown</span>
    </div>
    <svg class="w-3.5 h-3.5 text-stone-400 group-hover:text-[#61532E] transition-transform duration-300" id="chevron-sidebar-curated" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"></path></svg>
  </button>
  <div id="sidebar-curated-container" class="space-y-1.5 pt-2 overflow-hidden transition-all duration-300">
    <button class="w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50" data-curated-filter="links_layers" onclick="window.toggleSidebarCurated('links_layers')"><span>Links &amp; Layers</span><span class="text-[10px] text-stone-400 font-light">Chains &amp; links</span></button>
    <button class="w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50" data-curated-filter="drops_halo" onclick="window.toggleSidebarCurated('drops_halo')"><span>Drops &amp; Halo</span><span class="text-[10px] text-stone-400 font-light">Halo &amp; drops</span></button>
    <button class="w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50" data-curated-filter="dainty_steps" onclick="window.toggleSidebarCurated('dainty_steps')"><span>Dainty Steps</span><span class="text-[10px] text-stone-400 font-light">Anklets &amp; charms</span></button>
    <button class="w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50" data-curated-filter="daily_luxe" onclick="window.toggleSidebarCurated('daily_luxe')"><span>Daily Luxe</span><span class="text-[10px] text-stone-400 font-light">18K gold vermeil</span></button>
    <button class="w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50" data-curated-filter="tennis_fever" onclick="window.toggleSidebarCurated('tennis_fever')"><span>Tennis Fever</span><span class="text-[10px] text-stone-400 font-light">Tennis bracelets</span></button>
    <button class="w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50" data-curated-filter="heirloom_suites" onclick="window.toggleSidebarCurated('heirloom_suites')"><span>Heirloom Suites</span><span class="text-[10px] text-stone-400 font-light">Gift boxes &amp; sets</span></button>
  </div>
</div>"""

if "chevron-sidebar-curated" not in p_html:
    target_pos = p_html.find("<span>Bestsellers</span></button></div></div></aside>")
    if target_pos != -1:
        insert_idx = target_pos + len("<span>Bestsellers</span></button></div></div>")
        p_html = p_html[:insert_idx] + curated_sidebar_snippet + p_html[insert_idx:]
        with open('jewellery-design-html/products.html', 'w', encoding='utf-8') as f:
            f.write(p_html)
        print("Inserted Curated Collections dropdown into desktop sidebar in products.html!")
    else:
        print("WARNING: target position in products.html sidebar not found")


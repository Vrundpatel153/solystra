import os
import re

ROOT = os.path.abspath('.')

# ==============================================================================
# 1. UPDATE JS ACCORDION LOGIC IN app.js (Smooth Collapse-in/out, Not Instant)
# ==============================================================================
NEW_ACCORDION_JS = """  // Jewelry Category Metal Dropdowns (925 Silver & 18K Gold) with Smooth Transitions
  window.toggleCategoryDropdown = function (key, e) {
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
    const otherChevron = document.getElementById('chevron-' + otherKey);

    function closeAccordion(el, chev) {
      if (!el || el.classList.contains('hidden')) return;
      el.style.maxHeight = el.scrollHeight + 'px';
      el.style.opacity = '1';
      // Force repaint
      void el.offsetHeight;
      el.style.transition = 'max-height 0.45s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.35s ease, padding 0.35s ease';
      el.style.maxHeight = '0px';
      el.style.opacity = '0';
      el.style.paddingTop = '0px';
      el.style.paddingBottom = '0px';
      if (chev) {
        chev.style.transition = 'transform 0.45s cubic-bezier(0.22, 1, 0.36, 1)';
        chev.classList.remove('rotate-180', 'text-[#61532E]');
      }
      setTimeout(function () {
        el.classList.add('hidden');
        el.style.maxHeight = '';
        el.style.opacity = '';
        el.style.paddingTop = '';
        el.style.paddingBottom = '';
      }, 450);
    }

    function openAccordion(el, chev) {
      if (!el) return;
      el.classList.remove('hidden');
      el.style.maxHeight = '0px';
      el.style.opacity = '0';
      el.style.paddingTop = '0px';
      el.style.paddingBottom = '0px';
      // Force repaint
      void el.offsetHeight;
      const targetHeight = el.scrollHeight + 15;
      el.style.transition = 'max-height 0.45s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.35s ease, padding 0.35s ease';
      el.style.maxHeight = targetHeight + 'px';
      el.style.opacity = '1';
      el.style.paddingTop = key.startsWith('mob-') ? '8px' : '6px';
      el.style.paddingBottom = key.startsWith('mob-') ? '8px' : '6px';
      if (chev) {
        chev.style.transition = 'transform 0.45s cubic-bezier(0.22, 1, 0.36, 1)';
        chev.classList.add('rotate-180', 'text-[#61532E]');
      }
      setTimeout(function () {
        el.style.maxHeight = 'none';
      }, 450);
    }

    const isCurrentlyOpen = !subMenu.classList.contains('hidden') && subMenu.style.maxHeight !== '0px';

    if (isCurrentlyOpen) {
      closeAccordion(subMenu, chevron);
    } else {
      if (otherMenu) closeAccordion(otherMenu, otherChevron);
      openAccordion(subMenu, chevron);
    }
  };"""

for js_rel in ['jewellery-design-html/js/app.js', 'jewellery-design-html-dist/js/app.js']:
    js_path = os.path.join(ROOT, js_rel)
    if os.path.exists(js_path):
        with open(js_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
        
        # Replace existing toggleCategoryDropdown
        pat = r'// Jewelry Category Metal Dropdowns \(925 Silver & 18K Gold\)\s*window\.toggleCategoryDropdown = function.*?\n  \};\n'
        if re.search(pat, js_code, re.DOTALL):
            js_code = re.sub(pat, NEW_ACCORDION_JS + "\n", js_code, flags=re.DOTALL)
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_code)
            print(f"Updated JS accordion in {js_rel}")
        else:
            print(f"Could not find exact pattern in {js_rel}")

# ==============================================================================
# 2. UPDATE MENUBARS ACROSS ALL HTML FILES (Close Silver by default)
# ==============================================================================
def update_menubar_closed(content):
    # Desktop Silver: aria-expanded="false", chevron without rotate-180 text-[#61532E], submenu with hidden
    content = content.replace(
        'onclick="window.toggleCategoryDropdown(\'desktop-silver\', event)" type="button"><div class="flex items-center gap-2.5">',
        'onclick="window.toggleCategoryDropdown(\'desktop-silver\', event)" type="button" aria-expanded="false"><div class="flex items-center gap-2.5">'
    )
    content = content.replace('aria-expanded="true"', 'aria-expanded="false"')
    
    # Desktop Silver chevron
    content = content.replace(
        'id="chevron-desktop-silver" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 group-hover:text-[#61532E] transition-transform duration-300 rotate-180 text-[#61532E]"',
        'id="chevron-desktop-silver" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 group-hover:text-[#61532E] transition-transform duration-300"'
    )
    content = content.replace(
        'class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 group-hover:text-[#61532E] transition-transform duration-300 rotate-180 text-[#61532E]" fill="none" height="24" id="chevron-desktop-silver"',
        'class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 group-hover:text-[#61532E] transition-transform duration-300" fill="none" height="24" id="chevron-desktop-silver"'
    )
    
    # Desktop Silver Submenu: add hidden
    content = content.replace(
        'class="space-y-0.5 p-1.5 bg-white border-t border-[#CEBDA7]/60 transition-all duration-300" id="subcat-menu-desktop-silver"',
        'class="space-y-0.5 p-1.5 bg-white border-t border-[#CEBDA7]/60 transition-all duration-300 hidden" id="subcat-menu-desktop-silver"'
    )

    # Mobile Silver chevron
    content = content.replace(
        'id="chevron-mob-silver" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 transition-transform duration-300 rotate-180 text-[#61532E]"',
        'id="chevron-mob-silver" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg" class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 transition-transform duration-300"'
    )
    content = content.replace(
        'class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 transition-transform duration-300 rotate-180 text-[#61532E]" fill="none" height="24" id="chevron-mob-silver"',
        'class="lucide lucide-chevron-down w-3.5 h-3.5 text-stone-500 transition-transform duration-300" fill="none" height="24" id="chevron-mob-silver"'
    )

    # Mobile Silver Submenu: add hidden
    content = content.replace(
        'class="space-y-0.5 p-2 bg-white border-t border-[#CEBDA7]/60" id="subcat-menu-mob-silver"',
        'class="space-y-0.5 p-2 bg-white border-t border-[#CEBDA7]/60 hidden" id="subcat-menu-mob-silver"'
    )

    return content

# ==============================================================================
# 3. UPDATE PRODUCT CARDS (Remove reviews, add __% OFF, unify metal labels to #61532E)
# ==============================================================================
def update_product_card(card_html):
    # 1. Extract discount percentage
    disc_m = re.search(r'<span class="inline-flex items-center justify-center px-[^>]*>([0-9]+%\s*OFF)</span>', card_html)
    disc_text = disc_m.group(1) if disc_m else None
    
    if not disc_text:
        # Check if there is a badge or other discount
        disc_m2 = re.search(r'([0-9]+%\s*OFF)', card_html)
        disc_text = disc_m2.group(1) if disc_m2 else 'SPECIAL'

    # 2. Replace rating badge with discount badge
    rating_pat = r'<div class="inline-flex items-center gap-1 px-1\.5 sm:px-2 py-0\.5 rounded-lg bg-\[#FAF8F5\] border border-\[#CEBDA7\] shadow-2xs shrink-0"><svg class="w-3 h-3 sm:w-3\.5 sm:h-3\.5 fill-\[#C5A059\] text-\[#C5A059\][^>]*>.*?<polygon points="12 2[^>]*></polygon></svg><span class="font-sans font-bold text-\[10\.5px\] sm:text-xs text-stone-900 leading-none">[0-9\.]+</span></div>'
    new_disc_badge = f'<span class="inline-flex items-center justify-center px-1.5 sm:px-2 py-0.5 rounded-md bg-[#61532E]/10 border border-[#61532E]/25 text-[#61532E] font-sans font-bold text-[8.5px] sm:text-[9.5px] uppercase tracking-wider leading-none shadow-2xs shrink-0">{disc_text}</span>'
    card_html = re.sub(rating_pat, new_disc_badge, card_html)

    # 3. Replace metal badge with unified theme primary color #61532E badge
    # Matches Rose, Gold, Silver
    metal_pat = r'<div class="ml-auto shrink-0 flex items-center"><div class="inline-flex items-center gap-1 px-1\.5 sm:px-2 py-0\.5 rounded-lg border shadow-2xs select-none transition-transform duration-200 shrink-0"[^>]*title="([^"]*)"><span class="font-serif font-bold tracking-tight text-\[10px\] sm:text-\[11px\] leading-none text-\[#[A-Fa-f0-9]+\]">([0-9a-zA-Z]+)</span><span class="font-sans font-bold uppercase tracking-wider text-\[7\.5px\] sm:text-\[8\.5px\] leading-none text-\[#[A-Fa-f0-9]+\]">([A-Z\s]+)</span></div></div>'
    
    def repl_metal(m):
        title = m.group(1)
        code = m.group(2)
        label = m.group(3)
        return f'<div class="ml-auto shrink-0 flex items-center"><div class="inline-flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded-md border border-[#CEBDA7] bg-[#FAF8F5] shadow-2xs select-none transition-transform duration-200 shrink-0" title="{title}"><span class="font-serif font-bold tracking-tight text-[10px] sm:text-[11px] leading-none text-[#61532E]">{code}</span><span class="font-sans font-bold uppercase tracking-wider text-[7.5px] sm:text-[8.5px] leading-none text-[#61532E]">{label}</span></div></div>'

    card_html = re.sub(metal_pat, repl_metal, card_html)

    # 4. Remove redundant discount pill from bottom row
    old_disc_pill_pat = r'<span class="inline-flex items-center justify-center px-1\.5 xs:px-2 py-0\.5 sm:py-1 rounded-md sm:rounded-lg bg-\[#F6F3EE\] border border-\[#CEBDA7\] text-\[#61532E\] font-sans font-bold text-\[8\.5px\] xs:text-\[9\.5px\] sm:text-\[10px\] uppercase tracking-wide leading-none whitespace-nowrap shrink-0 shadow-2xs">[0-9]+%\s*OFF</span>'
    card_html = re.sub(old_disc_pill_pat, '', card_html)

    return card_html

def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update menubar
    content = update_menubar_closed(content)

    # 2. Update product cards
    # Pattern to match each product card
    card_regex = re.compile(r'(<div class="group bg-white rounded-2xl border border-\[#CEBDA7\][^>]*onclick="[^"]*product\.html\?id=[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>\s*</div>)', re.DOTALL)
    
    cards_found = 0
    def card_replacer(match):
        nonlocal cards_found
        cards_found += 1
        return update_product_card(match.group(1))

    content = card_regex.sub(card_replacer, content)

    # Also catch cards without onclick on root if any (e.g. index gala cards)
    card_regex2 = re.compile(r'(<div class="group bg-white rounded-2xl border border-\[#CEBDA7\][^>]*>.*?points="12 2.*?</div>\s*</div>\s*</div>\s*</div>)', re.DOTALL)
    content = card_regex2.sub(card_replacer, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Processed {file_path}: updated menubar and {cards_found} cards.")

# Run for all HTML files in both directories
for folder in ['jewellery-design-html', 'jewellery-design-html-dist']:
    dir_path = os.path.join(ROOT, folder)
    if os.path.exists(dir_path):
        for fname in os.listdir(dir_path):
            if fname.endswith('.html'):
                process_html_file(os.path.join(dir_path, fname))

print("Global product cards and menubar HTML update complete!")


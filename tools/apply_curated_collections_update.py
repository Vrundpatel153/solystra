#!/usr/bin/env python3
"""
apply_curated_collections_update.py
Applies the 5 client-specified curated collections across:
1. Menu Bar (Desktop Mega-Menu & Mobile Drawer)
2. Curated Collection (Top Collections Coverflow carousel on HomePage)
3. Footer (Desktop 4-column directory & Mobile accordion directory)
"""

import os
import re

# 5 Curated Collections
CURATED_COLLECTIONS = [
    {
        "title": "Links & Layers",
        "tag": "Chains &amp; Necklaces",
        "menu_desc": "Chains, chokers &amp; layered links",
        "mob_desc": "Chains, chokers &amp; links",
        "desc": "Interlocking links, sleek chains &amp; layered statement chokers.",
        "url": "products.html?category=necklaces",
        "react_url": "#/products?category=necklaces",
        "img": "solystra_assets/categories/zavya_style/chains.webp",
        "footer_label": "Links &amp; Layers (Chains)"
    },
    {
        "title": "Drops & Halo",
        "tag": "Rings &amp; Earrings",
        "menu_desc": "Halo rings, drops &amp; cocktail studs",
        "mob_desc": "Halo rings &amp; drops",
        "desc": "Starlight drops, halo solitaires &amp; radiant cocktail studs.",
        "url": "products.html?category=earrings",
        "react_url": "#/products?category=earrings",
        "img": "solystra_assets/collections/collection_drops.webp",
        "footer_label": "Drops &amp; Halo (Rings &amp; Earrings)"
    },
    {
        "title": "Dainty Steps",
        "tag": "Anklets &amp; Payals",
        "menu_desc": "Dainty anklets &amp; charm links",
        "mob_desc": "Dainty anklets &amp; charms",
        "desc": "Dainty bell charms, sleek shimmer links &amp; everyday payals.",
        "url": "products.html?category=anklets",
        "react_url": "#/products?category=anklets",
        "img": "solystra_assets/categories/zavya_style/anklets.webp",
        "footer_label": "Dainty Steps (Anklets)"
    },
    {
        "title": "Daily Luxe",
        "tag": "18K Gold Products",
        "menu_desc": "18K gold vermeil for everyday elegance",
        "mob_desc": "18K gold everyday",
        "desc": "18K Italian gold vermeil crafted for effortless everyday elegance.",
        "url": "products.html?metal=gold",
        "react_url": "#/products?metal=gold",
        "img": "solystra_assets/collections/collection_ombre.webp",
        "footer_label": "Daily Luxe (18K Gold Products)"
    },
    {
        "title": "Tennis Fever",
        "tag": "Tennis Bracelets",
        "menu_desc": "Tennis bracelets, crystal cuffs &amp; links",
        "mob_desc": "Tennis bracelets &amp; cuffs",
        "desc": "Continuous Austrian crystal tennis bracelets &amp; bold cuffs.",
        "url": "products.html?category=bracelets",
        "react_url": "#/products?category=bracelets",
        "img": "solystra_assets/categories/zavya_style/bracelets.webp",
        "footer_label": "Tennis Fever (Bracelets)"
    }
]

# Generate Desktop Nav HTML
desktop_nav_buttons = []
for c in CURATED_COLLECTIONS:
    btn = f'''<button class="w-full text-left py-2 px-2.5 -mx-2.5 rounded-xl hover:bg-[#F6F3EE] transition-all cursor-pointer group flex items-center justify-between" onclick="window.location.href='{c['url']}'"><div><div class="text-[13px] font-sans font-semibold text-stone-900 group-hover:text-[#61532E] transition-colors leading-tight">{c['title']}</div><div class="text-[11px] text-stone-400 font-light mt-0.5">{c['menu_desc']}</div></div><svg class="lucide lucide-chevron-right w-3.5 h-3.5 text-stone-300 group-hover:text-[#61532E] group-hover:translate-x-0.5 transition-all opacity-0 group-hover:opacity-100" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m9 18 6-6-6-6"></path></svg></button>'''
    desktop_nav_buttons.append(btn)

DESKTOP_NAV_CURATED = (
    '<div class="col-span-3 space-y-3 border-r border-[#CEBDA7]/80 pr-6">'
    '<div class="text-[11px] uppercase tracking-[0.2em] text-[#61532E] font-bold pb-2 border-b border-[#CEBDA7]/60">Curated Collections</div>'
    '<div class="space-y-0.5 pt-1">'
    + ''.join(desktop_nav_buttons)
    + '</div></div>'
)

# Generate Mobile Nav HTML
mobile_nav_buttons = []
for c in CURATED_COLLECTIONS:
    btn = f'''<button class="w-full text-left p-2 rounded-lg hover:bg-stone-100 flex items-center justify-between text-xs font-medium text-stone-800 cursor-pointer" onclick="window.location.href='{c['url']}'"><span>{c['title']}</span><span class="text-[10px] text-stone-400">{c['mob_desc']}</span></button>'''
    mobile_nav_buttons.append(btn)

MOBILE_NAV_CURATED = (
    '<div class="space-y-1 pb-3 border-b border-[#CEBDA7]">'
    '<div class="text-[11px] font-bold uppercase tracking-wider text-[#61532E] mb-1.5">Curated Collections</div>'
    '<div class="grid grid-cols-1 gap-1">'
    + ''.join(mobile_nav_buttons)
    + '</div></div>'
)

# Generate Desktop Footer HTML
desktop_footer_items = []
for c in CURATED_COLLECTIONS:
    desktop_footer_items.append(f'<li><a class="hover:text-[#61532E] transition-colors" href="{c["url"]}">{c["footer_label"]}</a></li>')
desktop_footer_items.append('<li><a class="hover:text-[#61532E] transition-colors" href="products.html?metal=silver">Pure 925 Silver Heirlooms</a></li>')

DESKTOP_FOOTER_COLLECTIONS = (
    '<h4 class="font-semibold text-stone-900 uppercase tracking-wider mb-4 text-xs">Collections</h4>'
    '<ul class="space-y-2.5 text-stone-600">'
    + ''.join(desktop_footer_items)
    + '</ul>'
)

# Generate Mobile Footer Accordion HTML
mobile_footer_items = []
for c in CURATED_COLLECTIONS:
    mobile_footer_items.append(f'<li><a class="block hover:text-[#61532E]" href="{c["url"]}">{c["footer_label"]}</a></li>')
mobile_footer_items.append('<li><a class="block hover:text-[#61532E]" href="products.html?metal=silver">Pure 925 Silver Heirlooms</a></li>')

MOBILE_FOOTER_ACCORDION = (
    '<div class="bg-white rounded-xl border border-stone-200/80 overflow-hidden shadow-2xs">'
    '<button onclick="window.toggleFooterAccordion && window.toggleFooterAccordion(\'collections\')" class="w-full px-4 py-3 flex items-center justify-between text-left font-semibold text-stone-900 uppercase tracking-wider text-[11px] cursor-pointer">'
    '<span>Collections</span>'
    '<svg class="lucide lucide-chevron-down w-4 h-4 text-stone-500 transition-transform duration-200" id="footer-accordion-collections-chevron" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="m6 9 6 6 6-6"></path></svg>'
    '</button>'
    '<ul id="footer-accordion-collections" class="px-4 pb-3.5 space-y-2 text-stone-600 text-[11.5px] border-t border-stone-100 pt-2.5 hidden">'
    + ''.join(mobile_footer_items)
    + '</ul>'
    '</div>'
)

# Generate Coverflow Cards for HomePage (5 collections repeated 5 times = 25 cards)
COVERFLOW_ITEMS = []
for loop in range(5):
    for i, c in enumerate(CURATED_COLLECTIONS):
        idx = loop * 5 + i
        card_html = (
            f'<div class="w-[66vw] xs:w-[60vw] sm:w-[250px] md:w-[280px] aspect-[303/423] shrink-0 snap-center relative rounded-[24px] sm:rounded-[28px] p-[2.5px] sm:p-[3px] bg-gradient-to-b from-[#D4AF37] via-[#61532E] to-[#3D341B] transition-all duration-500 ease-out cursor-pointer group select-none origin-center is-side" data-collection-card="true" data-index="{idx}" data-url="{c["url"]}">'
            f'<div class="w-full h-full rounded-[21.5px] sm:rounded-[25px] overflow-hidden bg-[#FAF8F5] relative">'
            f'<img alt="{c["title"]}" class="w-full h-full object-cover scale-[1.095] block pointer-events-none transition-transform duration-500 group-hover:scale-[1.13]" draggable="false" loading="lazy" src="{c["img"]}"/>'
            f'<div class="absolute inset-x-0 bottom-0 p-4 sm:p-5 bg-gradient-to-t from-black/85 via-black/45 to-transparent text-white pointer-events-none">'
            f'<span class="text-[9px] uppercase tracking-[0.2em] text-[#CEBDA7] font-semibold block">{c["tag"]}</span>'
            f'<h3 class="font-serif text-base sm:text-lg font-normal leading-tight text-white mt-0.5">{c["title"]}</h3>'
            f'<p class="text-[10px] text-stone-300 font-light mt-1 line-clamp-1 hidden sm:block">{c["desc"]}</p>'
            f'</div>'
            f'</div></div>'
        )
        COVERFLOW_ITEMS.append(card_html)

ALL_COVERFLOW_CARDS = ''.join(COVERFLOW_ITEMS)

def patch_file(filepath):
    if not os.path.isfile(filepath):
        print(f"Skipping missing {filepath}")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    # 1. Desktop Nav Curated Collections
    pattern_desk_nav = r'<div class="col-span-3 space-y-3 border-r border-\[#CEBDA7\]/80 pr-6"><div class="text-\[11px\] uppercase tracking-\[0\.2em\] text-\[#61532E\] font-bold pb-2 border-b border-\[#CEBDA7\]/60">Curated Collections</div>.*?</div></div>(?=\s*<div class="col-span-3 space-y-3 border-r border-\[#CEBDA7\]/80 pr-6">|\s*<div class="col-span-4 pl-6 border-r)'
    if re.search(pattern_desk_nav, content, re.DOTALL):
        content = re.sub(pattern_desk_nav, DESKTOP_NAV_CURATED, content, count=1, flags=re.DOTALL)
        print(f"  [{os.path.basename(filepath)}] Updated Desktop Nav Curated Collections")

    # 2. Mobile Nav Curated Collections
    pattern_mob_nav = r'<div class="space-y-1 pb-3 border-b border-\[#CEBDA7\]"><div class="text-\[11px\] font-bold uppercase tracking-wider text-\[#61532E\] mb-1\.5">Curated Collections</div>.*?</div></div>(?=\s*<div class="space-y-2 pb-3 border-b border-\[#CEBDA7\]"><div class="text-\[11px\] font-bold uppercase tracking-wider text-stone-900)'
    if re.search(pattern_mob_nav, content, re.DOTALL):
        content = re.sub(pattern_mob_nav, MOBILE_NAV_CURATED, content, count=1, flags=re.DOTALL)
        print(f"  [{os.path.basename(filepath)}] Updated Mobile Nav Curated Collections")

    # 3. Desktop Footer Collections
    pattern_desk_footer = r'<h4 class="font-semibold text-stone-900 uppercase tracking-wider mb-4 text-xs">Collections</h4>\s*<ul class="space-y-2\.5 text-stone-600">.*?</ul>'
    if re.search(pattern_desk_footer, content, re.DOTALL):
        content = re.sub(pattern_desk_footer, DESKTOP_FOOTER_COLLECTIONS, content, count=1, flags=re.DOTALL)
        print(f"  [{os.path.basename(filepath)}] Updated Desktop Footer Collections")

    # 4. Mobile Footer Collections Accordion
    pattern_mob_footer = r'<div class="bg-white rounded-xl border border-stone-200/80 overflow-hidden shadow-2xs"><button [^>]*><span>Collections</span>.*?</button>(?:\s*<ul[^>]*>.*?</ul>)?\s*</div>(?=\s*<div class="bg-white rounded-xl border border-stone-200/80 overflow-hidden shadow-2xs"><button [^>]*><span>Customer Care)'
    if re.search(pattern_mob_footer, content, re.DOTALL):
        content = re.sub(pattern_mob_footer, MOBILE_FOOTER_ACCORDION, content, count=1, flags=re.DOTALL)
        print(f"  [{os.path.basename(filepath)}] Updated Mobile Footer Accordion")

    # 5. Top Collections Coverflow on index.html
    if os.path.basename(filepath) == 'index.html':
        pattern_coverflow = r'(<div class="flex items-center gap-2 sm:gap-4 overflow-x-auto hide-scrollbar py-6 sm:py-8 px-\[17vw\] sm:px-\[calc\(50%-130px\)\] md:px-\[calc\(50%-145px\)\] snap-x snap-mandatory cursor-grab active:cursor-grabbing select-none" id="top-collections-scroll">).*?(?=</div></div></div></section>)'
        if re.search(pattern_coverflow, content, re.DOTALL):
            content = re.sub(pattern_coverflow, r'\g<1>' + ALL_COVERFLOW_CARDS, content, count=1, flags=re.DOTALL)
            print(f"  [{os.path.basename(filepath)}] Updated Top Collections Coverflow Cards (25 themed cards)")

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved {filepath}")
    else:
        print(f"No changes made to {filepath}")

def patch_app_js(filepath):
    if not os.path.isfile(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        js = f.read()
    orig = js

    # 1. Update coverflow activeIndex default to 12 (exact center of 25 cards)
    js = js.replace('let activeIndex = 11;', 'let activeIndex = 12;')
    js = js.replace('centerCardByIndex(11, false);', 'centerCardByIndex(12, false);')

    # 2. Support data-url on coverflow card click
    old_click = """card.addEventListener('click', function (e) {
        if (hasMoved) return; // Ignore drag clicks
        if (idx !== activeIndex) {
          e.preventDefault();
          centerCardByIndex(idx, true);
        } else {
          window.location.href = 'products.html';
        }
      });"""
    new_click = """card.addEventListener('click', function (e) {
        if (hasMoved) return; // Ignore drag clicks
        if (idx !== activeIndex) {
          e.preventDefault();
          centerCardByIndex(idx, true);
        } else {
          const targetUrl = card.getAttribute('data-url') || 'products.html';
          window.location.href = targetUrl;
        }
      });"""
    if old_click in js:
        js = js.replace(old_click, new_click)
        print(f"  [{os.path.basename(filepath)}] Updated coverflow card click navigation with data-url")

    # 3. Add toggleFooterAccordion
    if 'window.toggleFooterAccordion' not in js:
        footer_acc_func = """
  // Mobile Footer Accordion Toggle
  window.toggleFooterAccordion = function (name) {
    const el = document.getElementById('footer-accordion-' + name);
    const chev = document.getElementById('footer-accordion-' + name + '-chevron');
    if (!el) return;
    const isHidden = el.classList.contains('hidden');
    if (isHidden) {
      el.classList.remove('hidden');
      if (chev) {
        chev.classList.add('rotate-180');
        chev.classList.add('text-[#61532E]');
      }
    } else {
      el.classList.add('hidden');
      if (chev) {
        chev.classList.remove('rotate-180');
        chev.classList.remove('text-[#61532E]');
      }
    }
  };
"""
        # Insert before window.initApp or at end
        if 'window.initApp' in js:
            js = js.replace('window.initApp', footer_acc_func + '\n  window.initApp')
        else:
            js += '\n' + footer_acc_func
        print(f"  [{os.path.basename(filepath)}] Added window.toggleFooterAccordion")

    if js != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Saved {filepath}")

def main():
    html_files = [
        'categories.html',
        'index.html',
        'offers.html',
        'privacy.html',
        'product.html',
        'products.html',
        'terms.html'
    ]

    print("--- Patching jewellery-design-html ---")
    for f in html_files:
        patch_file(os.path.join('jewellery-design-html', f))
    patch_app_js(os.path.join('jewellery-design-html', 'js', 'app.js'))

    print("\n--- Patching jewellery-design-html-dist ---")
    for f in html_files:
        patch_file(os.path.join('jewellery-design-html-dist', f))
    patch_app_js(os.path.join('jewellery-design-html-dist', 'js', 'app.js'))

if __name__ == '__main__':
    main()


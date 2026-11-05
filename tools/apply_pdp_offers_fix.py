import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

css_rule = """
/* Available Offers Cards - 2.5 cards visible on mobile, 3-column grid on desktop */
.pdp-offer-card {
  flex: 0 0 calc((100% - 16px) / 2.45);
  min-width: 0;
  scroll-snap-align: start;
}

@media (min-width: 640px) {
  .pdp-offer-card {
    flex: 1 1 0% !important;
    width: 100% !important;
    min-width: 0 !important;
  }
}
"""

new_offers_html = """<div class="space-y-2 pt-1"><div class="text-xs font-semibold text-stone-900 tracking-wide flex items-center justify-between"><span>Available offers</span><span class="text-[10.5px] text-[#61532E] font-medium">Auto-applied at checkout</span></div><div class="flex sm:grid sm:grid-cols-3 gap-2 sm:gap-2.5 overflow-x-auto sm:overflow-visible hide-scrollbar py-1.5 px-1 -mx-1 snap-x snap-mandatory"><button class="pdp-offer-card p-2 sm:p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] hover:border-[#61532E] text-left hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 sm:shrink active:scale-98 shadow-2xs flex flex-col justify-between snap-start" type="button" onclick="window.usePromoCode &amp;&amp; window.usePromoCode('PREPAID100')" style="flex: 0 0 calc((100% - 16px) / 2.45); min-width: 0;"><div><div class="flex items-center justify-between gap-1"><p class="text-[11.5px] sm:text-xs font-bold text-stone-900 leading-tight">Flat ₹100 off</p><span class="text-[8px] sm:text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1 py-0.5 rounded shrink-0">PREPAID</span></div><p class="text-[9px] sm:text-[10.5px] text-stone-600 mt-1 leading-tight">On prepaid orders</p></div><div class="mt-2 text-[9.5px] sm:text-[10.5px] font-mono tracking-tight flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5"><span class="text-stone-700 text-[9px] sm:text-[10px]">use <strong class="text-[#61532E] font-bold">PREPAID100</strong></span><span class="text-[8.5px] sm:text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span></div></button><button class="pdp-offer-card p-2 sm:p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] hover:border-[#61532E] text-left hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 sm:shrink active:scale-98 shadow-2xs flex flex-col justify-between snap-start" type="button" onclick="window.usePromoCode &amp;&amp; window.usePromoCode('SOL5')" style="flex: 0 0 calc((100% - 16px) / 2.45); min-width: 0;"><div><div class="flex items-center justify-between gap-1"><p class="text-[11.5px] sm:text-xs font-bold text-stone-900 leading-tight">Get 5% off</p><span class="text-[8px] sm:text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1 py-0.5 rounded shrink-0">&gt; ₹5,000</span></div><p class="text-[9px] sm:text-[10.5px] text-stone-600 mt-1 leading-tight">On orders above ₹5k</p></div><div class="mt-2 text-[9.5px] sm:text-[10.5px] font-mono tracking-tight flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5"><span class="text-stone-700 text-[9px] sm:text-[10px]">use <strong class="text-[#61532E] font-bold">SOL5</strong></span><span class="text-[8.5px] sm:text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span></div></button><button class="pdp-offer-card p-2 sm:p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] hover:border-[#61532E] text-left hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 sm:shrink active:scale-98 shadow-2xs flex flex-col justify-between snap-start" type="button" onclick="window.usePromoCode &amp;&amp; window.usePromoCode('SOL10')" style="flex: 0 0 calc((100% - 16px) / 2.45); min-width: 0;"><div><div class="flex items-center justify-between gap-1"><p class="text-[11.5px] sm:text-xs font-bold text-stone-900 leading-tight">Get 10% off</p><span class="text-[8px] sm:text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1 py-0.5 rounded shrink-0">&gt; ₹10,000</span></div><p class="text-[9px] sm:text-[10.5px] text-stone-600 mt-1 leading-tight">On orders above ₹10k</p></div><div class="mt-2 text-[9.5px] sm:text-[10.5px] font-mono tracking-tight flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5"><span class="text-stone-700 text-[9px] sm:text-[10px]">use <strong class="text-[#61532E] font-bold">SOL10</strong></span><span class="text-[8.5px] sm:text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span></div></button></div></div>"""

def update_css(path):
    if not os.path.exists(path):
        print("CSS not found:", path)
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '.pdp-offer-card' in content:
        # replace existing definition
        import re
        content = re.sub(r'/\* Available Offers Cards[^*]*\*/\s*\.pdp-offer-card\s*\{[^}]+\}\s*@media[^{]+\{\s*\.pdp-offer-card\s*\{[^}]+\}\s*\}', '', content)
    content += '\n' + css_rule.strip() + '\n'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated CSS:", path)

def update_html(path):
    if not os.path.exists(path):
        print("HTML not found:", path)
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    idx = content.find('Available offers')
    if idx == -1:
        print("Available offers not found in:", path)
        return
    
    parent_start = content.rfind('<div class="space-y-2', 0, idx)
    parent_end = content.find('</button></div></div>', idx) + len('</button></div></div>')
    
    content = content[:parent_start] + new_offers_html + content[parent_end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated HTML:", path)

# 1. Update CSS files
update_css('jewellery-design-html/css/styles.css')
update_css('jewellery-design-html-dist/css/styles.css')
update_css(r'C:\Users\vrund\OneDrive\Desktop\solystra-html\css\styles.css')

# 2. Update HTML files
update_html('jewellery-design-html/product.html')
update_html('jewellery-design-html-dist/product.html')
update_html(r'C:\Users\vrund\OneDrive\Desktop\solystra-html\product.html')

print("All Vanilla files updated successfully!")


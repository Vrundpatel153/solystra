with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the counter and dots in index.html
old_curated_nav = '''<span class="text-xs font-mono text-stone-500" id="curated-combo-counter">
                Combo 01 / 03
              </span>
<!-- Dot Indicators -->
<div class="flex items-center gap-1.5" id="curated-combo-dots">
<button aria-label="Go to combo 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-5 bg-[#61532E]" data-combo-dot="0" type="button"></button>
<button aria-label="Go to combo 2" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-1.5 bg-stone-300 hover:bg-stone-400" data-combo-dot="1" type="button"></button>
<button aria-label="Go to combo 3" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-1.5 bg-stone-300 hover:bg-stone-400" data-combo-dot="2" type="button"></button>
</div>'''

new_curated_nav = '''<span class="text-xs font-mono text-stone-500" id="curated-combo-counter">
                Combo 01 / 02
              </span>
<!-- Dot Indicators -->
<div class="flex items-center gap-1.5" id="curated-combo-dots">
<button aria-label="Go to combo 1" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-5 bg-[#61532E]" data-combo-dot="0" type="button"></button>
<button aria-label="Go to combo 2" class="h-1.5 rounded-full transition-all duration-300 cursor-pointer w-1.5 bg-stone-300 hover:bg-stone-400" data-combo-dot="1" type="button"></button>
</div>'''

if old_curated_nav in text:
    text = text.replace(old_curated_nav, new_curated_nav)
    with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully updated curated nav in index.html!")
else:
    print("Could not find exact old_curated_nav match, let's search flexibly...")
    import re
    m = re.search(r'<span class="text-xs font-mono text-stone-500" id="curated-combo-counter">.*?</div>', text, re.DOTALL)
    if m:
        print("Found regex match:\n", m.group(0))
        text = text.replace(m.group(0), new_curated_nav)
        with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Updated via regex match!")
    else:
        print("Regex match also failed!")

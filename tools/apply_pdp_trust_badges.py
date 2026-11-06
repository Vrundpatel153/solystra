with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('7-Day Exchanges')
s = text.rfind('<div class="grid grid-cols-4', 0, idx)
e = text.find('</div>', text.find('1-Year Warranty', idx)) + len('</div>')
e = text.find('</div>', e) + len('</div>')

old_badges = text[s:e]

new_badges = """<div class="grid grid-cols-4 gap-2 sm:gap-3 py-1">
      <!-- 1. Insured Delivery -->
      <div class="flex flex-col items-center justify-start text-center cursor-default group">
        <div class="w-8.5 h-8.5 sm:w-10 sm:h-10 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shadow-2xs mb-1.5 transition-colors group-hover:border-[#61532E]">
          <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/>
            <path d="M15 18H9"/>
            <path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.63l-3.24-4.05A1 1 0 0 0 17.76 8H14v10"/>
            <circle cx="7" cy="18" r="2"/>
            <circle cx="17" cy="18" r="2"/>
          </svg>
        </div>
        <span class="text-[10px] sm:text-xs font-semibold text-stone-800 leading-tight">Insured Delivery</span>
      </div>

      <!-- 2. BIS 925 Hallmark -->
      <div class="flex flex-col items-center justify-start text-center cursor-default group">
        <div class="w-8.5 h-8.5 sm:w-10 sm:h-10 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shadow-2xs mb-1.5 transition-colors group-hover:border-[#61532E]">
          <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="m9 12 2 2 4-4"/>
          </svg>
        </div>
        <span class="text-[10px] sm:text-xs font-semibold text-stone-800 leading-tight">BIS 925 Hallmark</span>
      </div>

      <!-- 3. 7-Day Exchanges -->
      <div class="flex flex-col items-center justify-start text-center cursor-default group">
        <div class="w-8.5 h-8.5 sm:w-10 sm:h-10 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shadow-2xs mb-1.5 transition-colors group-hover:border-[#61532E]">
          <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
            <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
            <path d="M16 21h5v-5"/>
          </svg>
        </div>
        <span class="text-[10px] sm:text-xs font-semibold text-stone-800 leading-tight">7-Day Exchanges</span>
      </div>

      <!-- 4. 1-Year Warranty -->
      <div class="flex flex-col items-center justify-start text-center cursor-default group">
        <div class="w-8.5 h-8.5 sm:w-10 sm:h-10 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shadow-2xs mb-1.5 transition-colors group-hover:border-[#61532E]">
          <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <circle cx="12" cy="8" r="6"/>
            <path d="m15.48 12.89 1.52 8.53a.5.5 0 0 1-.81.47L12 19.2l-4.19 2.69a.5.5 0 0 1-.81-.47l1.52-8.53"/>
          </svg>
        </div>
        <span class="text-[10px] sm:text-xs font-semibold text-stone-800 leading-tight">1-Year Warranty</span>
      </div>
    </div>"""

assert old_badges in text, "old badges not found"
text = text.replace(old_badges, new_badges, 1)

with open('jewellery-design-html/product.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated product.html trust badges successfully!")

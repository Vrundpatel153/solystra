with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('7-Day Exchanges')
sec_start = text.rfind('<section', 0, idx)
sec_end = text.find('</section>', idx) + len('</section>')

old_section = text[sec_start:sec_end]

new_section = """<section class="py-2 sm:py-2.5 lg:py-3 bg-white border-y border-[#CEBDA7]/50 shadow-[0_1px_4px_rgba(0,0,0,0.02)]">
  <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
    <div class="grid grid-cols-4 items-center divide-x divide-[#CEBDA7]/35">
      
      <!-- 1. Insured Delivery -->
      <div class="flex flex-col sm:flex-row items-center justify-center px-1 sm:px-3 lg:px-4 py-0.5 sm:py-1 gap-1 sm:gap-2.5 group cursor-default text-center sm:text-left">
        <div class="w-6.5 h-6.5 min-[360px]:w-7 min-[360px]:h-7 sm:w-8.5 sm:h-8.5 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shrink-0 shadow-2xs group-hover:border-[#61532E] transition-colors">
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/>
            <path d="M15 18H9"/>
            <path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.63l-3.24-4.05A1 1 0 0 0 17.76 8H14v10"/>
            <circle cx="7" cy="18" r="2"/>
            <circle cx="17" cy="18" r="2"/>
          </svg>
        </div>
        <div class="leading-tight">
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline">Insured</span>
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline sm:ml-0.5">Delivery</span>
        </div>
      </div>

      <!-- 2. BIS 925 Hallmark -->
      <div class="flex flex-col sm:flex-row items-center justify-center px-1 sm:px-3 lg:px-4 py-0.5 sm:py-1 gap-1 sm:gap-2.5 group cursor-default text-center sm:text-left">
        <div class="w-6.5 h-6.5 min-[360px]:w-7 min-[360px]:h-7 sm:w-8.5 sm:h-8.5 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shrink-0 shadow-2xs group-hover:border-[#61532E] transition-colors">
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="m9 12 2 2 4-4"/>
          </svg>
        </div>
        <div class="leading-tight">
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline">BIS 925</span>
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline sm:ml-0.5">Hallmark</span>
        </div>
      </div>

      <!-- 3. 7-Day Exchanges -->
      <div class="flex flex-col sm:flex-row items-center justify-center px-1 sm:px-3 lg:px-4 py-0.5 sm:py-1 gap-1 sm:gap-2.5 group cursor-default text-center sm:text-left">
        <div class="w-6.5 h-6.5 min-[360px]:w-7 min-[360px]:h-7 sm:w-8.5 sm:h-8.5 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shrink-0 shadow-2xs group-hover:border-[#61532E] transition-colors">
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M3 12a9 9 0 0 1 15-6.7L21 8"/>
            <path d="M21 3v5h-5"/>
            <path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>
            <path d="M3 21v-5h5"/>
          </svg>
        </div>
        <div class="leading-tight">
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline">7-Day</span>
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline sm:ml-0.5">Exchanges</span>
        </div>
      </div>

      <!-- 4. 1-Year Warranty -->
      <div class="flex flex-col sm:flex-row items-center justify-center px-1 sm:px-3 lg:px-4 py-0.5 sm:py-1 gap-1 sm:gap-2.5 group cursor-default text-center sm:text-left">
        <div class="w-6.5 h-6.5 min-[360px]:w-7 min-[360px]:h-7 sm:w-8.5 sm:h-8.5 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] shrink-0 shadow-2xs group-hover:border-[#61532E] transition-colors">
          <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <circle cx="12" cy="8" r="6"/>
            <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>
          </svg>
        </div>
        <div class="leading-tight">
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline">1-Year</span>
          <span class="text-[9.5px] min-[360px]:text-[10px] sm:text-xs lg:text-[13px] font-semibold text-stone-800 tracking-tight sm:tracking-normal whitespace-nowrap block sm:inline sm:ml-0.5">Warranty</span>
        </div>
      </div>

    </div>
  </div>
</section>"""

text = text[:sec_start] + new_section + text[sec_end:]

with open('jewellery-design-html/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html trust section successfully!")

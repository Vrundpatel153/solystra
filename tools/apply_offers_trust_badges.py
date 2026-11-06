with open('jewellery-design-html/offers.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = text.find('BIS 925 Hallmarked')
if m != -1:
    s = text.rfind('<section', 0, m)
    e = text.find('</section>', m) + len('</section>')
    print('Found offers.html trust section!')
    
    new_offers_section = """<section class="py-4 sm:py-6 bg-white border-b border-[#CEBDA7]/50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
      <div class="p-2 flex flex-col items-center">
        <div class="w-9 h-9 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] mb-2 shadow-2xs">
          <svg class="w-4.5 h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="m9 12 2 2 4-4"/>
          </svg>
        </div>
        <h5 class="font-serif text-xs sm:text-sm font-semibold text-stone-900">BIS 925 Hallmarked</h5>
        <p class="text-[11px] text-stone-500 font-light mt-0.5">Government certified stamp</p>
      </div>

      <div class="p-2 flex flex-col items-center">
        <div class="w-9 h-9 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] mb-2 shadow-2xs">
          <svg class="w-4.5 h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/>
            <path d="M15 18H9"/>
            <path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.63l-3.24-4.05A1 1 0 0 0 17.76 8H14v10"/>
            <circle cx="7" cy="18" r="2"/>
            <circle cx="17" cy="18" r="2"/>
          </svg>
        </div>
        <h5 class="font-serif text-xs sm:text-sm font-semibold text-stone-900">Insured Delivery</h5>
        <p class="text-[11px] text-stone-500 font-light mt-0.5">Free express across India</p>
      </div>

      <div class="p-2 flex flex-col items-center">
        <div class="w-9 h-9 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] mb-2 shadow-2xs">
          <svg class="w-4.5 h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
            <path d="M3 3v5h5"/>
            <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/>
            <path d="M16 21h5v-5"/>
          </svg>
        </div>
        <h5 class="font-serif text-xs sm:text-sm font-semibold text-stone-900">7-Day Exchanges</h5>
        <p class="text-[11px] text-stone-500 font-light mt-0.5">Hassle-free doorstep pickup</p>
      </div>

      <div class="p-2 flex flex-col items-center">
        <div class="w-9 h-9 rounded-full bg-[#FAF8F5] border border-[#CEBDA7]/80 flex items-center justify-center text-[#61532E] mb-2 shadow-2xs">
          <svg class="w-4.5 h-4.5 text-[#61532E]" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" viewBox="0 0 24 24">
            <circle cx="12" cy="8" r="6"/>
            <path d="m15.48 12.89 1.52 8.53a.5.5 0 0 1-.81.47L12 19.2l-4.19 2.69a.5.5 0 0 1-.81-.47l1.52-8.53"/>
          </svg>
        </div>
        <h5 class="font-serif text-xs sm:text-sm font-semibold text-stone-900">1-Year Warranty</h5>
        <p class="text-[11px] text-stone-500 font-light mt-0.5">Anti-tarnish replating guarantee</p>
      </div>
    </div>
  </div>
</section>"""
    old_section = text[s:e]
    text = text.replace(old_section, new_offers_section, 1)
    with open('jewellery-design-html/offers.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated offers.html trust section successfully!")


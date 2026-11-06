import sys

sys.stdout.reconfigure(encoding='utf-8')

# The craftsmanship badges strip to insert right inside <div class="flex-1 space-y-4"> after the main image container
craftsmanship_strip = '''<div class="hidden sm:grid grid-cols-3 gap-2.5 pt-1">
<div class="p-2.5 rounded-xl bg-white border border-[#CEBDA7]/70 shadow-2xs text-center flex flex-col items-center justify-center">
<svg class="w-4 h-4 text-[#61532E] mb-1 stroke-[1.8]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="m9 12 2 2 4-4"></path></svg>
<span class="text-[10.5px] font-bold text-stone-900 leading-tight">BIS 925 Hallmark</span>
<span class="text-[9px] text-stone-500 mt-0.5">Certified Pure Silver</span>
</div>
<div class="p-2.5 rounded-xl bg-white border border-[#CEBDA7]/70 shadow-2xs text-center flex flex-col items-center justify-center">
<svg class="w-4 h-4 text-[#61532E] mb-1 stroke-[1.8]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><rect height="14" rx="2" width="20" x="2" y="7"></rect><path d="M12 7v14"></path><path d="M2 12h20"></path><path d="M7.5 7a2.5 2.5 0 0 1 0-5A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"></path></svg>
<span class="text-[10.5px] font-bold text-stone-900 leading-tight">Velvet Keepsake</span>
<span class="text-[9px] text-stone-500 mt-0.5">Signature Gift Box</span>
</div>
<div class="p-2.5 rounded-xl bg-white border border-[#CEBDA7]/70 shadow-2xs text-center flex flex-col items-center justify-center">
<svg class="w-4 h-4 text-[#61532E] mb-1 stroke-[1.8]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2v20"></path><path d="m4.93 4.93 4.24 4.24"></path><path d="m14.83 14.83 4.24 4.24"></path><path d="M2 12h20"></path><path d="m4.93 19.07 4.24-4.24"></path><path d="m14.83 9.17 4.24-4.24"></path></svg>
<span class="text-[10.5px] font-bold text-stone-900 leading-tight">Lifetime Replating</span>
<span class="text-[9px] text-stone-500 mt-0.5">Free Polish & Care</span>
</div>
</div>
<div class="hidden sm:flex items-center gap-3 p-3 rounded-xl bg-[#FAF6F0] border border-[#CEBDA7] shadow-2xs">
<div class="w-7 h-7 rounded-full bg-[#61532E]/10 flex items-center justify-center text-[#61532E] shrink-0 font-serif font-bold text-[11px] border border-[#61532E]/25">925</div>
<div class="text-[11px] leading-tight">
<p class="font-bold text-stone-900">Official BIS Hallmark Authenticity Verification</p>
<p class="text-stone-600 mt-0.5 text-[10px]">Individually laser-engraved with serialized purity certificate &amp; master silversmith hallmark.</p>
</div>
</div>'''

target_marker = '</div></div></div></div><div class="lg:col-span-5'
# The left gallery ends with: </div></div></div></div><div class="lg:col-span-5
# Where the outer div is pdp-fixed-gallery, inner is flex-1 space-y-4, inner is aspect-square

for path in [
    'jewellery-design-html/product.html',
    'jewellery-design-html-dist/product.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\product.html'
]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if target_marker in content and 'Official BIS Hallmark Authenticity Verification' not in content:
        replacement = f'{craftsmanship_strip}</div></div></div><div class="lg:col-span-5'
        content = content.replace(target_marker, replacement)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path} with craftsmanship assurance strip!")
    else:
        print(f"Already updated or target not found in {path}")


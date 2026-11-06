import os
import re

targets = [
    'jewellery-design-html/index.html',
    'jewellery-design-html-dist/index.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\index.html'
]

old_grid = '<div class="hidden sm:grid sm:grid-cols-12 h-full w-full">'
new_grid = '<div class="solystra-hero-desktop-grid">'

old_card = '<div class="sm:col-span-6 lg:col-span-5 h-full flex flex-col justify-center px-8 sm:px-10 lg:px-14 bg-[#161412] relative z-10 border-r border-[#2C2723]/60">'
new_card = '<div class="solystra-hero-card">'

old_img_col = '<div class="sm:col-span-6 lg:col-span-7 h-full relative overflow-hidden bg-black">'
new_img_col = '<div class="solystra-hero-img-col">'

for t in targets:
    if not os.path.exists(t):
        continue
    with open(t, 'r', encoding='utf-8') as f:
        c = f.read()
    
    c = c.replace(old_grid, new_grid)
    c = c.replace(old_card, new_card)
    c = c.replace(old_img_col, new_img_col)
    
    with open(t, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated markup classes in {t}")

print("Hero markup classes updated!")

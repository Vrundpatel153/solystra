import re

with open('jewellery-design-html/index.html', encoding='utf-8') as f:
    text = f.read()

print("--- Hero banner images in index.html ---")
# find <picture> or <img> inside hero section
hero_idx = text.find('id="hero-section"')
if hero_idx == -1:
    hero_idx = text.find('id="hero-banner"')
if hero_idx == -1:
    hero_idx = text.find('hero-slider')

print("Hero section search near hero-slides:")
slides_idx = text.find('id="hero-slides"')
if slides_idx != -1:
    print(text[slides_idx:slides_idx+4000])

print("\n--- Collections section in index.html ---")
col_idx = text.find('id="collections-section"')
if col_idx == -1:
    col_idx = text.find('id="collections"')
if col_idx == -1:
    col_idx = text.find('Curated Collections')
if col_idx != -1:
    print(text[col_idx-100:col_idx+3500])


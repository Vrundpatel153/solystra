with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_start = text.find('Curated Looks')
if idx_start == -1:
    idx_start = text.find('CURATED LOOKS')
if idx_start == -1:
    idx_start = text.find('curated-look')
if idx_start == -1:
    idx_start = text.find('curated')

print("Found at:", idx_start)
section_start = text.rfind('<section', 0, idx_start)
section_end = text.find('</section>', idx_start) + len('</section>')

curated_section = text[section_start:section_end]
print("Section length:", len(curated_section))
print("First 1500 chars:\n", curated_section[:1500])

with open('scratch/current_curated_section.html', 'w', encoding='utf-8') as out:
    out.write(curated_section)


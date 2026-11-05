import re

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find category cards in index.html
matches = re.findall(r'<div class="[^"]*group[^"]*"(?:(?!<div class="[^"]*group[^"]*").)*?solystra_assets/(?:categories|collections)/[^"]*', c, re.DOTALL)
print(f"Index.html matches: {len(matches)}")

for i, m in enumerate(matches):
    img = re.search(r'src="([^"]*)"', m)
    img_str = img.group(1) if img else "no img"
    title = re.search(r'<(?:h3|h4|span|div)[^>]*class="[^"]*(?:font-serif|font-sans|font-semibold|font-medium)[^"]*"[^>]*>(.*?)</', m)
    title_str = title.group(1) if title else "no title"
    print(f"Match {i+1}: {title_str} -> {img_str}")


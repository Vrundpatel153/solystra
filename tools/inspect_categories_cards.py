import re

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find cards
cards = re.findall(r'<div[^>]*class="[^"]*group[^"]*"[^>]*>.*?</div>\s*</div>', c, re.DOTALL)
print(f"Group cards found: {len(cards)}")

# Check href or onclick in main content
main_start = c.find('<main')
main_end = c.find('</main>')
if main_start != -1 and main_end != -1:
    main_content = c[main_start:main_end]
    links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', main_content, re.DOTALL)
    print(f"Links in main: {len(links)}")
    for href, text in links[:20]:
        t = re.sub(r'<[^>]*>', '', text).strip()
        print(f"  href: {href} | text: {t[:30]}")
    
    # Check for any card elements with onclick or without links
    card_divs = re.findall(r'<div[^>]*onclick="([^"]*)"[^>]*>', main_content)
    print(f"Divs with onclick: {len(card_divs)}")
    for oc in card_divs:
        print(f"  onclick: {oc}")


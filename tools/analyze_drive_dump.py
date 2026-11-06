with open('jewellery-design-html/index.html') as f: pass # dummy

import urllib.request
import re

url = 'https://drive.google.com/drive/folders/11uGB087Uruph7Xj9M_JEybPUL5Z4lqW0'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Save to scratch to analyze
with open('scratch/drive_html_dump.txt', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved scratch/drive_html_dump.txt, size:", len(html))

# search for keywords
for kw in ['DSC', 'IMG', 'folder', '11uGB087Uruph7Xj9M_JEybPUL5Z4lqW0', 'thumbnail']:
    matches = [m.start() for m in re.finditer(re.escape(kw), html, re.I)]
    print(f"Keyword '{kw}': {len(matches)} occurrences")
    if matches:
        first = matches[0]
        print(f"  Snippet: {html[max(0, first-50):first+150]}")


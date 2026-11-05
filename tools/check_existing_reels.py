import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="video-reels-scroll"')
end_idx = text.find('</div></div></section>', idx)
section = text[idx:end_idx]

import re
titles = re.findall(r'<p class="text-xs[^>]+title="([^"]+)"', section)
print("Titles found:", len(titles))
for i, t in enumerate(titles[:15]):
    print(f"{i+1}: {t}")


with open('tools/hero_section_original.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
tags = re.findall(r'<section|<div id="[^"]+"', text)
print("Tags found:", tags[:20])
print("First 1000 chars:")
print(text[:1000])


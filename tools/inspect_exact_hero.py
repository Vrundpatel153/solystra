with open('tools/hero_section_exact.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
slides = re.findall(r'<div [^>]*id="hero-slide-\d".*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', text, re.DOTALL)
for i, s in enumerate(slides):
    print(f"=== SLIDE {i} ===")
    print(s)

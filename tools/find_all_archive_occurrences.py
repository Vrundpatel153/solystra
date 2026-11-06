with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# find all occurrences of "Explore All Categories Archive" with 300 chars before and after
for i, m in enumerate(re.finditer(r'Explore All Categories Archive', content)):
    start = max(0, m.start() - 350)
    end = min(len(content), m.end() + 350)
    print(f"\n--- Occurrence #{i+1} at index {m.start()} ---")
    print(content[start:end])


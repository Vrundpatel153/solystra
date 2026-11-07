with open('scratch/drive_root_script.txt', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# find all strings
strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', c)
print('Total strings found:', len(strings))

keywords = ['banner', 'category', 'collection', 'folder', 'image', 'hero', '1g8z', 'dsc', 'png', 'jpg', 'webp']
for s in strings:
    if any(k in s.lower() for k in keywords):
        print(' -', s)


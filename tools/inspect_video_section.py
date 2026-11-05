import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="video-reels-scroll"')
if idx != -1:
    parent_start = text.rfind('<section', 0, idx)
    parent_end = text.find('</section>', idx) + len('</section>')
    print("Length of section:", parent_end - parent_start)
    print("--- SECTION START ---")
    print(text[parent_start:parent_start+3000])


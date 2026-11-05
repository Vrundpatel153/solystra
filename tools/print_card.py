import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="video-reels-scroll"')
card_start = text.find('<div class="w-[205px]', idx)
card_end = text.find('<div class="w-[205px]', card_start + 1)
print(text[card_start:card_end])

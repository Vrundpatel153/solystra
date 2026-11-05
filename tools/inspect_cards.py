import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="video-reels-scroll"')
end_idx = text.find('</div></div></section>', idx)
section = text[idx:end_idx]

# Let's count how many video cards there are
import re
videos = re.findall(r'<video[^>]+>', section)
print(f"Total video tags in video-reels-scroll: {len(videos)}")
for i, v in enumerate(videos[:5]):
    print(f"Video {i+1}: {v}")

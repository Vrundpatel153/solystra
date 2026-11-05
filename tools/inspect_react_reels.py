import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src/pages/HomePage.jsx', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('const VIDEO_REELS =')
end_idx = text.find('];', idx) + 2
print(text[idx:end_idx])


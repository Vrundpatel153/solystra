import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request(
    'https://solystra.netlify.app',
    headers={'User-Agent': 'Mozilla/5.0'}
)
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

idx = html.find('data-hero-slide="0"')
s_start = html.rfind('<section', 0, idx)
s_end = html.find('</section>', idx)
print("=== LIVE NETLIFY HERO SECTION ===")
print(html[s_start:s_end+10])


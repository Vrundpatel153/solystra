import urllib.request
import re

url = 'https://drive.google.com/drive/folders/1IzLhq3kwsNxt8HgckZP65nVgne4dRPZF'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Subfolder 1IzLhq3kwsNxt8HgckZP65nVgne4dRPZF HTML length: {len(html)}")
        with open('scratch/subfolder_heart_raw.txt', 'w', encoding='utf-8') as f:
            f.write(html)
            
        labels = re.findall(r'aria-label="([^"]+)"', html)
        print(f"Total aria-labels in Heart Raw: {len(labels)}")
        for l in labels:
            if any(k in l.lower() for k in ['dsc', 'img', 'folder', 'shared', 'raw', 'jpg', 'png']):
                print("  ", l)
except Exception as e:
    print("Error:", e)


import os

photos = sorted(os.listdir('scratch/drive_photos'))
count = len(photos)
html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Drive Photos Gallery</title>
<style>
  body {{ font-family: sans-serif; background: #1a1715; color: #fff; padding: 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
  .card {{ background: #2a2420; border-radius: 12px; overflow: hidden; padding: 12px; border: 1px solid #443c35; }}
  img {{ width: 100%; height: 320px; object-fit: cover; border-radius: 8px; }}
  h4 {{ margin: 10px 0 4px; font-size: 14px; }}
</style>
</head>
<body>
<h1>Solystra Drive Photos ({count} images)</h1>
<div class="grid">
"""

for p in photos:
    html += f"""
  <div class="card">
    <img src="drive_photos/{p}" alt="{p}">
    <h4>{p}</h4>
  </div>
"""

html += """
</div>
</body>
</html>
"""

with open('scratch/gallery.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Gallery generated at scratch/gallery.html")

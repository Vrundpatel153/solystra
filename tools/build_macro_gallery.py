import os

thumb_dir = 'jewellery-design-html/drive_thumbs'
files = [f"DSC0{i}.JPG" for i in range(3000, 3118) if os.path.exists(os.path.join(thumb_dir, f"DSC0{i}.JPG"))]

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Macro Still Life Audit (3000-3117)</title>
<style>
  body { background: #111; color: #fff; font-family: sans-serif; padding: 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
  .card { background: #1a1a1a; border-radius: 8px; overflow: hidden; border: 1px solid #333; text-align: center; }
  img { width: 100%; height: 140px; object-fit: contain; background: #000; }
  .name { padding: 8px; font-size: 13px; font-weight: bold; color: #C5A059; }
</style>
</head>
<body>
<h1>Solystra Still-Life & Macro Assets (DSC03000 - DSC03117)</h1>
<p>Total items: """ + str(len(files)) + """</p>
<div class="grid">
"""

for f in files:
    html += f"""
    <div class="card">
      <img src="drive_thumbs/{f}" alt="{f}" />
      <div class="name">{f}</div>
    </div>
    """

html += """
</div>
</body>
</html>
"""

with open('jewellery-design-html/macro_gallery.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Created jewellery-design-html/macro_gallery.html")


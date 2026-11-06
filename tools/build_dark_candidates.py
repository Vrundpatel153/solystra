import os

thumb_dir = 'jewellery-design-html/drive_thumbs'
candidates = [
    'DSC02719.JPG', 'DSC02720.JPG', 'DSC02730.JPG', 'DSC02738.JPG', 'DSC02739.JPG',
    'DSC02845.JPG', 'DSC02846.JPG', 'DSC02850.JPG', 'DSC02855.JPG',
    'DSC02910.JPG', 'DSC02915.JPG', 'DSC02920.JPG', 'DSC02925.JPG', 'DSC02930.JPG'
]

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Dark Editorial Model Candidates for Hero Banner</title>
<style>
  body { background: #0c0b0a; color: #fff; font-family: sans-serif; padding: 24px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
  .card { background: #161514; border: 1px solid #332f2a; border-radius: 8px; overflow: hidden; text-align: center; }
  img { width: 100%; height: 200px; object-fit: contain; background: #000; }
  .name { padding: 10px; font-size: 14px; font-weight: bold; color: #D4AF37; }
</style>
</head>
<body>
<h1>Naturally Dark Editorial Model Shots from Drive</h1>
<p>These shots naturally have deep charcoal/black backgrounds straight out of the camera, eliminating the need for any synthetic paint blocks!</p>
<div class="grid">
"""

for f in candidates:
    if os.path.exists(os.path.join(thumb_dir, f)):
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

with open('jewellery-design-html/dark_model_candidates.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Created jewellery-design-html/dark_model_candidates.html")


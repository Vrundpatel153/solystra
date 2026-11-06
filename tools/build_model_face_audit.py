import os
import shutil

src_dir = 'scratch/model_candidates'
dst_dir = 'jewellery-design-html/model_candidates_thumbs'
os.makedirs(dst_dir, exist_ok=True)

for f in os.listdir(src_dir):
    if f.endswith('.JPG'):
        shutil.copy2(os.path.join(src_dir, f), os.path.join(dst_dir, f))

# Also add chosen hero models
for f in os.listdir('scratch/chosen_hero_models'):
    if f.endswith('.jpg'):
        shutil.copy2(os.path.join('scratch/chosen_hero_models', f), os.path.join(dst_dir, f))

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Model Face & Jewelry Framing Audit</title>
<style>
  body { background: #111; color: #fff; font-family: sans-serif; padding: 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
  .card { background: #1a1a1a; border-radius: 8px; overflow: hidden; border: 1px solid #333; text-align: center; }
  img { width: 100%; height: 280px; object-fit: contain; background: #000; display: block; }
  .name { padding: 8px; font-size: 13px; font-weight: bold; color: #D4AF37; }
</style>
</head>
<body>
<h1>Model Face &amp; Jewelry Framing Inspection</h1>
<div class="grid">
"""

for f in sorted(os.listdir(dst_dir)):
    if f.lower().endswith(('.jpg', '.webp')):
        html += f"""
        <div class="card">
          <img src="model_candidates_thumbs/{f}" alt="{f}" />
          <div class="name">{f}</div>
        </div>
        """

html += """
</div>
</body>
</html>
"""

with open('jewellery-design-html/model_face_audit.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Created jewellery-design-html/model_face_audit.html")


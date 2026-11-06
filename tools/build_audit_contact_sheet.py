import os
import shutil
import json

src_dir = 'scratch/drive_thumbnails'
dst_dir = 'jewellery-design-html/drive_thumbs'
os.makedirs(dst_dir, exist_ok=True)

# Copy thumbnails to jewellery-design-html/drive_thumbs
for f in os.listdir(src_dir):
    if f.upper().endswith('.JPG'):
        src_path = os.path.join(src_dir, f)
        dst_path = os.path.join(dst_dir, f)
        if not os.path.exists(dst_path):
            shutil.copy2(src_path, dst_path)

print(f"Copied thumbnails to {dst_dir}")

with open('scratch/catalog_398_audit.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Group by series
series_map = {}
for item in catalog:
    s = item['series']
    if s not in series_map:
        series_map[s] = []
    series_map[s].append(item)

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Solystra Art Direction: Full 398 Google Drive Photos Audit</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #121212; color: #E5E5E5; margin: 0; padding: 24px; }
  h1 { font-size: 24px; color: #D4AF37; margin-bottom: 8px; }
  p.subtitle { color: #A0A0A0; font-size: 14px; margin-bottom: 24px; }
  .series-title { font-size: 18px; color: #FAF8F5; border-bottom: 1px solid #333; padding-bottom: 6px; margin-top: 32px; margin-bottom: 16px; display: flex; justify-content: space-between; }
  .series-title span { font-size: 13px; color: #C5A059; font-weight: normal; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
  .card { background: #1E1E1E; border-radius: 8px; overflow: hidden; border: 1px solid #2A2A2A; transition: transform 0.2s, border-color 0.2s; cursor: pointer; }
  .card:hover { transform: translateY(-3px); border-color: #D4AF37; }
  .img-box { width: 100%; height: 180px; background: #0A0A0A; display: flex; items-center; justify-content: center; overflow: hidden; position: relative; }
  .img-box img { width: 100%; height: 100%; object-fit: cover; }
  .meta { padding: 8px; font-size: 11px; }
  .meta .name { font-weight: 600; color: #FFF; font-size: 12px; }
  .meta .info { color: #888; margin-top: 2px; }
  .tag { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 500; margin-top: 4px; }
  .tag-land { background: #1A365D; color: #90CDF4; }
  .tag-port { background: #2A4365; color: #BEE3F8; }
  .tag-square { background: #22543D; color: #9AE6B4; }
</style>
</head>
<body>
  <h1>Solystra Atelier: Comprehensive 398 Drive Photos Audit</h1>
  <p class="subtitle">Complete visual audit of all 398 authentic photoshoot assets (DSC02719 to DSC03117) directly from the Google Drive archive.</p>
"""

for series_name, items in series_map.items():
    html += f'<div class="series-title">{series_name} <span>({len(items)} photos)</span></div>\n'
    html += '<div class="grid">\n'
    for it in items:
        f = it['filename']
        orient = it['orientation']
        tag_cls = "tag-land" if orient == "landscape" else ("tag-port" if orient == "portrait" else "tag-square")
        html += f"""
        <div class="card" title="{f}">
          <div class="img-box">
            <img src="drive_thumbs/{f}" alt="{f}" loading="lazy" />
          </div>
          <div class="meta">
            <div class="name">{f}</div>
            <div class="info">{it['w']}x{it['h']} ({orient})</div>
            <span class="tag {tag_cls}">{orient}</span>
          </div>
        </div>
        """
    html += '</div>\n'

html += """
</body>
</html>
"""

with open('jewellery-design-html/drive_audit_contact_sheet.html', 'w', encoding='utf-8') as f_out:
    f_out.write(html)

print("Created jewellery-design-html/drive_audit_contact_sheet.html")


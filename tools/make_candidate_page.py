import os

# Let's write an interactive candidate gallery to review
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Category & Collection Candidates from Drive</title>
<style>
  body { font-family: sans-serif; background: #18181b; color: #fff; padding: 24px; }
  h1 { color: #C5A059; }
  h2 { color: #f5e6cc; border-bottom: 1px solid #444; padding-bottom: 6px; margin-top: 24px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
  .item { background: #27272a; border-radius: 8px; overflow: hidden; border: 1px solid #3f3f46; text-align: center; }
  .item img { width: 100%; height: 140px; object-fit: cover; }
  .item span { display: block; font-size: 11px; padding: 4px; color: #a1a1aa; }
</style>
</head>
<body>
<h1>Drive Photos Candidates for Categories & Collections</h1>
"""

series_picks = {
    "1. Necklaces & Pendants (Yellow Top & Neck Series)": [f"DSC0{n}.JPG" for n in range(2720, 2765, 3)],
    "2. Earrings & Solitaires (Black Blazer Series)": [f"DSC0{n}.JPG" for n in range(2805, 2870, 3)],
    "3. Bracelets, Kadas & Tennis Links (Sage Green Series)": [f"DSC0{n}.JPG" for n in range(2905, 2965, 3)],
    "4. Rings & Finger Solitaires (Hand Poses & Macro)": [f"DSC0{n}.JPG" for n in range(2965, 3010, 3)],
    "5. Suites, Gift Boxes & Velvet Macro (Still Life Series)": [f"DSC0{n}.JPG" for n in range(3015, 3075, 3)],
    "6. Lookbook & Signature Collections": [f"DSC0{n}.JPG" for n in range(3100, 3118, 2)]
}

for title, fnames in series_picks.items():
    html += f"<h2>{title}</h2><div class='grid'>"
    for fn in fnames:
        p = os.path.join('jewellery-design-html/drive_thumbs', fn)
        if os.path.exists(p):
            html += f"<div class='item'><img src='drive_thumbs/{fn}' alt='{fn}'/><span>{fn}</span></div>"
    html += "</div>"

html += "</body></html>"

with open('jewellery-design-html/category_curation_candidates.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Created category_curation_candidates.html")

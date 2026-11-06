import os

candidates = {
    'Bracelets & Kadas': [
        ('DSC03087.JPG', 'Macro Austrian Diamond Tennis Bracelet on dark velvet'),
        ('DSC03085.JPG', 'Minimalist Tennis Bracelet horizontal lineup'),
        ('DSC02915.JPG', 'Model close-up of wrist wearing Tennis Bracelet (Sage Green)')
    ],
    'Rings & Bands': [
        ('DSC03013.JPG', 'Solitaire & Crown Cocktail Ring in velvet setting'),
        ('DSC03011.JPG', 'Handcrafted Ring macro perspective'),
        ('DSC03116.JPG', 'Single Diamond Solitaire Ring on dark studio')
    ],
    'Earrings & Studs': [
        ('DSC03001.JPG', 'Austrian Diamond Starlight Drop Earring (Vertical)'),
        ('DSC03109.JPG', 'Sparkling Chandelier Studs macro'),
        ('DSC03075.JPG', 'Minimalist Solitaire Studs')
    ],
    'Necklaces & Pendants': [
        ('DSC03100.JPG', 'Classic Austrian Solitaire Riviera Tennis Necklace'),
        ('DSC02721.JPG', 'Model wearing Bespoke Heart Solitaire Pendant (Yellow Dress)'),
        ('DSC02810.JPG', 'Model wearing Layered Pearl & Dancing Solitaire (Black Blazer)')
    ],
    'Anklets & Payals': [
        ('DSC03040.JPG', 'Delicate Shimmer Link Chain with drop charms'),
        ('DSC03064.JPG', 'Dainty Link Chain flat-lay on dark velvet')
    ],
    'Gift Sets & Complete Suites': [
        ('DSC03045.JPG', 'Complete Atelier Solitaire Suite (Necklace + Earrings + Ring)'),
        ('DSC03070.JPG', 'Heirloom Diamond Suite in Luxury Box Setting'),
        ('DSC03090.JPG', 'Signature Lookbook Ensemble')
    ]
}

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Solystra Art Director Selection: Final Category & Hero Candidates</title>
<style>
  body { background: #0E0D0C; color: #FAF8F5; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; padding: 32px; max-width: 1200px; margin: auto; }
  h1 { font-family: Georgia, serif; color: #D4AF37; font-weight: normal; margin-bottom: 6px; }
  p.desc { color: #A09A8E; font-size: 14px; margin-bottom: 32px; }
  .section { margin-bottom: 40px; background: #161514; border: 1px solid #2B2824; border-radius: 12px; padding: 24px; }
  .section-title { font-size: 18px; color: #E8D8B8; font-weight: 600; margin-bottom: 16px; border-bottom: 1px solid #332F2A; padding-bottom: 8px; }
  .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; }
  .item-card { background: #1F1D1A; border: 1px solid #3A352E; border-radius: 8px; overflow: hidden; }
  .item-card img { width: 100%; height: 180px; object-fit: contain; background: #090909; display: block; }
  .item-info { padding: 12px; }
  .item-name { font-weight: 600; color: #D4AF37; font-size: 13px; }
  .item-desc { font-size: 12px; color: #B5AEA4; margin-top: 4px; line-height: 1.4; }
  .badge { display: inline-block; background: #61532E; color: #FFF; font-size: 10px; padding: 2px 8px; border-radius: 4px; margin-top: 8px; }
</style>
</head>
<body>
  <h1>Solystra Atelier Selection Audit</h1>
  <p class="desc">Senior Marketer &amp; Art Director curation from all 398 authentic Google Drive photoshoot assets. ZERO mockups, ZERO pink Zavya placeholders.</p>
"""

for cat, items in candidates.items():
    html += f'<div class="section"><div class="section-title">{cat}</div><div class="cards-grid">'
    for idx, (fname, desc) in enumerate(items):
        is_rec = (idx == 0)
        badge_text = "★ RECOMMENDED FOR CATEGORY CARD" if is_rec else "ALTERNATIVE CANDIDATE"
        badge_style = "background: #8A6D3B; color: #FFF;" if is_rec else "background: #2D2A26; color: #A09A8E;"
        html += f"""
        <div class="item-card">
          <img src="drive_thumbs/{fname}" alt="{fname}" />
          <div class="item-info">
            <div class="item-name">{fname}</div>
            <div class="item-desc">{desc}</div>
            <span class="badge" style="{badge_style}">{badge_text}</span>
          </div>
        </div>
        """
    html += '</div></div>'

html += """
</body>
</html>
"""

with open('jewellery-design-html/curated_selection_preview.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved jewellery-design-html/curated_selection_preview.html")


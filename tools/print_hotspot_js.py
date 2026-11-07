with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Click to view piece' in line or 'activeHotspot' in line or 'renderHotspots' in line or 'styling-combos' in line or 'curated-looks' in line:
        start = max(0, i - 30)
        end = min(len(lines), i + 70)
        print(f"=== Found around line {i+1} ===")
        print("".join(lines[start:end]))
        break

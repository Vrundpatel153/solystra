with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'banner_pc_' in line or 'banner_mob_' in line or 'banner_floral' in line or 'banner_profile' in line:
        start = max(0, i - 10)
        end = min(len(lines), i + 25)
        print(f"=== Match around line {i+1} ===")
        print("".join(lines[start:end]))


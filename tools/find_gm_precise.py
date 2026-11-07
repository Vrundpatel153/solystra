from PIL import Image

im = Image.open('scratch/curated_raw/golden_meadow_set_combo.png').convert('RGB')
w, h = im.size

# Search bright spots around ears (y: 400-800, x: 200-800)
ear_spots = []
for y in range(400, 800, 2):
    for x in range(250, 750, 2):
        r, g, b = im.getpixel((x, y))
        br = (r + g + b) / 3
        if br > 210:
            ear_spots.append((x, y, br, (r, g, b)))

print(f"Total bright spots in GM ear region: {len(ear_spots)}")
for s in sorted(ear_spots, key=lambda p: p[2], reverse=True)[:10]:
    print(f"GM Ear spot at x={s[0]}, y={s[1]}: rgb={s[3]}")

# Search bright spots around necklace / choker (y: 850-1400, x: 200-800)
neck_spots = []
for y in range(850, 1400, 2):
    for x in range(250, 750, 2):
        r, g, b = im.getpixel((x, y))
        br = (r + g + b) / 3
        if br > 210:
            neck_spots.append((x, y, br, (r, g, b)))

print(f"\nTotal bright spots in GM neck region: {len(neck_spots)}")
for s in sorted(neck_spots, key=lambda p: p[2], reverse=True)[:15]:
    print(f"GM Neck spot at x={s[0]}, y={s[1]}: rgb={s[3]}")


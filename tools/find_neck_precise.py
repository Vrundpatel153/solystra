from PIL import Image

im = Image.open('scratch/curated_raw/second_combo.png').convert('RGB')
w, h = im.size

# Search bright spots around chest / necklace
neck_spots = []
for y in range(850, 1400, 2):
    for x in range(300, 750, 2):
        r, g, b = im.getpixel((x, y))
        br = (r + g + b) / 3
        if br > 210:
            neck_spots.append((x, y, br, (r, g, b)))

print(f"Total bright spots in neck region: {len(neck_spots)}")
for s in sorted(neck_spots, key=lambda p: p[2], reverse=True)[:20]:
    print(f"Neck spot at x={s[0]}, y={s[1]}: rgb={s[3]}")


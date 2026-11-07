from PIL import Image

im = Image.open('scratch/curated_raw/second_combo.png').convert('RGB')
w, h = im.size

# Search brightest spots
bright_spots = []
for y in range(250, 700, 2):
    for x in range(450, 800, 2):
        r, g, b = im.getpixel((x, y))
        br = (r + g + b) / 3
        if br > 200:
            bright_spots.append((x, y, br, (r, g, b)))

print(f"Total bright spots in face/ear region: {len(bright_spots)}")
# Group by x, y
# Earring will be a distinct cluster of metallic/bright pixels
for s in sorted(bright_spots, key=lambda p: p[2], reverse=True)[:20]:
    print(f"Bright spot at x={s[0]}, y={s[1]}: rgb={s[3]}")


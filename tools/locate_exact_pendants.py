from PIL import Image

# Let's inspect where the necklace is in c2
im_c2 = Image.open('scratch/curated_raw/second_combo.png')
# In c2, the necklace has interlocking rings
# Let's check y from 800 to 1200
for y in range(800, 1300, 50):
    cr = im_c2.crop((350, y, 650, y + 50))
    # check brightness / yellow
    pixels = list(cr.getdata())
    brights = [p for p in pixels if (p[0] > 180 and p[1] > 140 and p[0] - p[2] > 40)]
    print(f"c2 y={y} to {y+50}: {len(brights)} gold-like pixels")

print("\n--- Golden Meadow ---")
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png')
for y in range(800, 1300, 50):
    cr = im_gm.crop((300, y, 700, y + 50))
    pixels = list(cr.getdata())
    brights = [p for p in pixels if (p[0] > 180 and p[1] > 140 and p[0] - p[2] > 40)]
    print(f"gm y={y} to {y+50}: {len(brights)} gold-like pixels")


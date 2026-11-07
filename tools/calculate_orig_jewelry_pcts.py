from PIL import Image

# C2 Earring: crop was from x: 550 to 650, y: 380 to 480
# Find center of the gold hoop earring
ear_im = Image.open('scratch/c2_exact_earring_zoom.jpg')
w_e, h_e = ear_im.size
ear_gold = []
for y in range(h_e):
    for x in range(w_e):
        r, g, b = ear_im.getpixel((x, y))
        # Gold hoop is bright yellow/gold
        if r > 180 and g > 130 and r - b > 40:
            ear_gold.append((550 + x, 380 + y))

avg_ear_x = sum(p[0] for p in ear_gold) / len(ear_gold)
avg_ear_y = sum(p[1] for p in ear_gold) / len(ear_gold)
print(f"C2 Earring in original (1024x1536): x={avg_ear_x:.1f}px ({avg_ear_x/1024*100:.2f}%), y={avg_ear_y:.1f}px ({avg_ear_y/1536*100:.2f}%)")

# C2 Pendant: crop was from x: 380 to 520, y: 950 to 1100
pend_im = Image.open('scratch/c2_exact_pendant_zoom.jpg')
w_p, h_p = pend_im.size
pend_gold = []
for y in range(h_p):
    for x in range(w_p):
        r, g, b = pend_im.getpixel((x, y))
        if r > 180 and g > 130 and r - b > 35:
            pend_gold.append((380 + x, 950 + y))

avg_pend_x = sum(p[0] for p in pend_gold) / len(pend_gold)
avg_pend_y = sum(p[1] for p in pend_gold) / len(pend_gold)
print(f"C2 Pendant in original (1024x1536): x={avg_pend_x:.1f}px ({avg_pend_x/1024*100:.2f}%), y={avg_pend_y:.1f}px ({avg_pend_y/1536*100:.2f}%)")

# GM Choker / Necklace:
# Let's inspect where the central drop/choker is:
chok_im = Image.open('scratch/gm_exact_choker_zoom.jpg')
w_c, h_c = chok_im.size
chok_gold = []
for y in range(h_c):
    for x in range(w_c):
        r, g, b = chok_im.getpixel((x, y))
        if (r > 180 and g > 130 and r - b > 35) or (r > 220 and g > 210 and b > 200):
            chok_gold.append((440 + x, 980 + y))
avg_chok_x = sum(p[0] for p in chok_gold) / len(chok_gold)
avg_chok_y = sum(p[1] for p in chok_gold) / len(chok_gold)
print(f"GM Central Necklace in original: x={avg_chok_x:.1f}px ({avg_chok_x/1024*100:.2f}%), y={avg_chok_y:.1f}px ({avg_chok_y/1536*100:.2f}%)")


from PIL import Image, ImageDraw

im_c2 = Image.open('scratch/curated_raw/second_combo.png').convert('RGB')
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png').convert('RGB')

# Let's inspect user's uploaded screenshots:
# In media_1794059940599_1e7a0564.png:
# C2 model is smiling to the left.
# Her earring is the gold hoop on her right ear (screen right).
# Her necklace is the gold chain with the interlocking circle pendant at the bottom.
# Let's find exact center of that gold hoop earring:
# Let's crop x: 550 to 650, y: 380 to 480
crop_ear_c2 = im_c2.crop((550, 380, 650, 480))
crop_ear_c2.save('scratch/c2_exact_earring_zoom.jpg')

# Let's crop necklace pendant: x: 380 to 520, y: 950 to 1100
crop_pendant_c2 = im_c2.crop((380, 950, 520, 1100))
crop_pendant_c2.save('scratch/c2_exact_pendant_zoom.jpg')

# In GM (Golden Meadow):
# Model facing front.
# Her choker / necklace is around y: 900 to 1150
# Golden flower on necklace: x: 300 to 400, y: 950 to 1050
# Central necklace loop: x: 450 to 550, y: 1000 to 1150
crop_choker_gm = im_gm.crop((440, 980, 580, 1120))
crop_choker_gm.save('scratch/gm_exact_choker_zoom.jpg')

crop_flower_gm = im_gm.crop((300, 930, 420, 1050))
crop_flower_gm.save('scratch/gm_exact_flower_zoom.jpg')

print("Saved exact jewelry zoom crops!")


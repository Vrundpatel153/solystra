from PIL import Image

im_c2 = Image.open('scratch/curated_raw/second_combo.png')
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png')

print("C2 size:", im_c2.size)
print("GM size:", im_gm.size)

# In C2:
# Top of hair: ~120px
# Earring: x=580px, y=420px
# Necklace chain: y=800-950px
# Necklace pendant: x=440px, y=1020px
# Below necklace: y=1150px
# Total vertical span needed: from y=100 to y=1180 -> height = 1080px (out of 1536)
# Width: x=100 to 950 -> width = 850px (out of 1024)
# Aspect ratio of needed region: 850 / 1080 = 0.787 (almost exactly 4:5 or 3:4!)

# In GM:
# Top of hair: ~180px
# Earrings: x=340px and x=670px, y=560-640px
# Necklace flowers: x=330px to 620px, y=940-1080px
# Necklace bottom drop: y=1150px
# Total vertical span needed: from y=150 to y=1200 -> height = 1050px (out of 1536)
# Width: x=150 to 870 -> width = 720px
# Aspect ratio of needed region: 720 / 1050 = 0.686 (around 2:3 or 3:4!)


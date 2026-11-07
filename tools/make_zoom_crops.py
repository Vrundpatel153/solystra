from PIL import Image

im = Image.open('scratch/curated_raw/second_combo.png')
w, h = im.size

# Let's crop from x: 45% to 65%, y: 40% to 65%
# In thumbnail, her ear is at middle-right of her face
crop_ear = im.crop((int(w * 0.45), int(h * 0.45), int(w * 0.65), int(h * 0.65)))
crop_ear.save('scratch/c2_ear_zoom.jpg')

# Let's crop her neck: from x: 40% to 70%, y: 65% to 90%
crop_neck = im.crop((int(w * 0.35), int(h * 0.65), int(w * 0.75), int(h * 0.90)))
crop_neck.save('scratch/c2_neck_zoom.jpg')

# Now let's do golden meadow:
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png')
w_gm, h_gm = im_gm.size

# In golden meadow thumbnail, she is facing front
# Earring is hanging on left and right ears
# Choker is around her neck
crop_gm_choker = im_gm.crop((int(w_gm * 0.30), int(h_gm * 0.60), int(w_gm * 0.70), int(h_gm * 0.85)))
crop_gm_choker.save('scratch/gm_choker_zoom.jpg')

print("Zoom crops saved!")


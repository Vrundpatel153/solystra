from PIL import Image

# Let's inspect raw image coordinates first
# Image is 1024 x 1536
im_c2 = Image.open('scratch/curated_raw/second_combo.png')
w_c2, h_c2 = im_c2.size

# In second combo.png:
# Where is the earring? Where is the necklace?
# Let's crop vertical strips to locate them
earring_crop_c2 = im_c2.crop((int(w_c2 * 0.45), int(h_c2 * 0.45), int(w_c2 * 0.65), int(h_c2 * 0.65)))
earring_crop_c2.save('scratch/c2_earring_test.jpg')

neck_crop_c2 = im_c2.crop((int(w_c2 * 0.35), int(h_c2 * 0.70), int(w_c2 * 0.75), int(h_c2 * 0.95)))
neck_crop_c2.save('scratch/c2_neck_test.jpg')

# In golden meadow:
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png')
w_gm, h_gm = im_gm.size

# Face is centered, let's look at ears and neck
ear_crop_gm = im_gm.crop((int(w_gm * 0.15), int(h_gm * 0.45), int(w_gm * 0.40), int(h_gm * 0.70)))
ear_crop_gm.save('scratch/gm_ear_test.jpg')

choker_crop_gm = im_gm.crop((int(w_gm * 0.35), int(h_gm * 0.70), int(w_gm * 0.65), int(h_gm * 0.95)))
choker_crop_gm.save('scratch/gm_choker_test.jpg')

print("Saved test crops for c2 and gm.")


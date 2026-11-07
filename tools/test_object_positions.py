from PIL import Image

im_c2 = Image.open('scratch/curated_raw/second_combo.png')
w, h = im_c2.size
print("Combo 2 size:", w, h)

# In Combo 2 (1024 x 1536):
# Where is the top of her head?
# Where are her earrings?
# Where is the bottom of her necklace?

# Let's test container aspect ratios:
# Mobile: 358 x 380 (ratio 0.942)
# Desktop: 592 x 430 (ratio 1.377) -> or if taller: 592 x 480 (ratio 1.233), 592 x 520 (ratio 1.138)

# Let's simulate CSS object-fit: cover with different object-position Y %
def simulate_cover(im, target_w, target_h, pos_y_pct):
    orig_w, orig_h = im.size
    # cover scale
    scale = max(target_w / orig_w, target_h / orig_h)
    scaled_w = int(orig_w * scale)
    scaled_h = int(orig_h * scale)
    
    scaled = im.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    
    # crop box
    crop_x = (scaled_w - target_w) // 2
    max_crop_y = scaled_h - target_h
    crop_y = int(max_crop_y * (pos_y_pct / 100.0))
    
    return scaled.crop((crop_x, crop_y, crop_x + target_w, crop_y + target_h))

# Test for C2 on Desktop (592 x 430) at pos_y: 30%, 50%, 65%, 80%, 90%
for pos in [40, 50, 60, 70, 80]:
    out = simulate_cover(im_c2, 592, 430, pos)
    out.save(f"scratch/c2_sim_desktop_pos{pos}.jpg")

# Test for GM on Desktop (592 x 430) at pos_y: 40%, 50%, 60%, 70%, 80%
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png')
for pos in [40, 50, 60, 70, 80]:
    out = simulate_cover(im_gm, 592, 430, pos)
    out.save(f"scratch/gm_sim_desktop_pos{pos}.jpg")

print("Saved simulations for desktop pos 40-80")


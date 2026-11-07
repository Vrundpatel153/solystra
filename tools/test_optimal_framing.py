from PIL import Image

im_c2 = Image.open('scratch/curated_raw/second_combo.png')
im_gm = Image.open('scratch/curated_raw/golden_meadow_set_combo.png')

def test_framing(im, name, w, h, obj_pos_pct):
    orig_w, orig_h = im.size
    scale = max(w / orig_w, h / orig_h)
    sc_w, sc_h = int(orig_w * scale), int(orig_h * scale)
    scaled = im.resize((sc_w, sc_h), Image.Resampling.LANCZOS)
    
    crop_x = (sc_w - w) // 2
    max_crop_y = sc_h - h
    crop_y = int(max_crop_y * (obj_pos_pct / 100.0))
    
    res = scaled.crop((crop_x, crop_y, crop_x + w, crop_y + h))
    return res

# Desktop tests: 592 x 460, 592 x 480, 592 x 500 at pos 40, 50, 60
for height in [460, 480, 500, 520]:
    for pos in [45, 55, 65]:
        c2 = test_framing(im_c2, 'c2', 592, height, pos)
        c2.save(f"scratch/c2_h{height}_p{pos}.jpg")
        gm = test_framing(im_gm, 'gm', 592, height, pos)
        gm.save(f"scratch/gm_h{height}_p{pos}.jpg")

# Mobile tests: 358 x 420, 358 x 450, 358 x 480 at pos 45, 55, 65
for height in [400, 440, 480]:
    for pos in [45, 55, 65]:
        c2 = test_framing(im_c2, 'c2', 358, height, pos)
        c2.save(f"scratch/c2_mob_h{height}_p{pos}.jpg")
        gm = test_framing(im_gm, 'gm', 358, height, pos)
        gm.save(f"scratch/gm_mob_h{height}_p{pos}.jpg")

print("Generated all framing test combinations!")


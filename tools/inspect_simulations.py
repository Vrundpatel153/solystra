from PIL import Image

# Let's inspect the crops of pos 50, 60, 70, 80
for pos in [50, 60, 70, 80]:
    c2 = Image.open(f"scratch/c2_sim_desktop_pos{pos}.jpg")
    gm = Image.open(f"scratch/gm_sim_desktop_pos{pos}.jpg")
    print(f"Pos {pos}%: C2 size {c2.size}, GM size {gm.size}")

# Let's also test taller container: 592 x 490 or 592 x 500
for pos in [50, 60, 70]:
    out_c2 = Image.open('scratch/curated_raw/second_combo.png')
    # simulate for 592 x 490
    scale = max(592 / 1024, 490 / 1536)
    sc_w, sc_h = int(1024 * scale), int(1536 * scale)
    sc = out_c2.resize((sc_w, sc_h), Image.Resampling.LANCZOS)
    crop_x = (sc_w - 592) // 2
    crop_y = int((sc_h - 490) * (pos / 100.0))
    cr = sc.crop((crop_x, crop_y, crop_x + 592, crop_y + 490))
    cr.save(f"scratch/c2_tall490_pos{pos}.jpg")
    
print("Saved tall tests")


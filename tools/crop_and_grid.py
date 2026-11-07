from PIL import Image, ImageDraw

im = Image.open("C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/calibration_loaded.jpg")

# The page has:
# h1, h2, then row 1:
# box-c2-mob: 358x380
# box-c2-pc: 592x430
# Let's find their coordinates by cropping regions

crop_c2_mob = im.crop((20, 150, 20 + 360, 150 + 382))
crop_c2_pc = im.crop((410, 150, 410 + 594, 150 + 432))

# Add grid to crop_c2_mob and crop_c2_pc
def add_grid(crop, filename):
    w, h = crop.size
    draw = ImageDraw.Draw(crop)
    for x_pct in range(0, 101, 10):
        x = int(w * x_pct / 100)
        draw.line([(x, 0), (x, h)], fill=(255, 255, 0, 120), width=1)
        draw.text((x + 2, 4), f"{x_pct}%", fill=(255, 255, 0))
    for y_pct in range(0, 101, 10):
        y = int(h * y_pct / 100)
        draw.line([(0, y), (w, y)], fill=(255, 255, 0, 120), width=1)
        draw.text((4, y + 2), f"{y_pct}%", fill=(255, 255, 0))
    crop.save(f"scratch/{filename}", quality=90)
    print(f"Saved scratch/{filename}")

add_grid(crop_c2_mob, "calib_c2_mob.jpg")
add_grid(crop_c2_pc, "calib_c2_pc.jpg")

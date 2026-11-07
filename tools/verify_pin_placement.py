from PIL import Image, ImageDraw

def draw_test_pin(filename, pins, out_name):
    im = Image.open(f"scratch/{filename}").convert('RGB')
    w, h = im.size
    draw = ImageDraw.Draw(im)
    for p in pins:
        x = int(w * p['x'] / 100)
        y = int(h * p['y'] / 100)
        r = 10
        # Draw outer glowing ring
        draw.ellipse([(x - r, y - r), (x + r, y + r)], outline=(212, 175, 55), width=3)
        draw.ellipse([(x - 3, y - 3), (x + 3, y + 3)], fill=(255, 255, 255))
        # Draw label
        draw.text((x + 14, y - 6), p['label'], fill=(255, 215, 0))
    im.save(f"scratch/{out_name}", quality=95)
    print(f"Saved scratch/{out_name}")

# C2 Mobile
draw_test_pin("calib_c2_mob.jpg", [
    {'x': 54.4, 'y': 50.6, 'label': 'Earrings'},
    {'x': 50.5, 'y': 70.6, 'label': 'Necklace'}
], "pin_test_c2_mob.jpg")

# C2 Desktop
draw_test_pin("calib_c2_pc.jpg", [
    {'x': 54.8, 'y': 47.6, 'label': 'Earrings'},
    {'x': 51.3, 'y': 75.5, 'label': 'Necklace'}
], "pin_test_c2_pc.jpg")

# GM Mobile
draw_test_pin("calib_gm_mob.jpg", [
    {'x': 54.4, 'y': 74.0, 'label': 'Choker & Earrings Set'}
], "pin_test_gm_mob.jpg")

# GM Desktop
draw_test_pin("calib_gm_pc.jpg", [
    {'x': 53.2, 'y': 72.4, 'label': 'Choker & Earrings Set'}
], "pin_test_gm_pc.jpg")


from PIL import Image, ImageDraw, ImageFont
import os

im = Image.open("C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/calibration_overview.jpg")

boxes = {
    "c2_mob": (28, 217, 28 + 361, 217 + 383),
    "c2_pc": (419, 217, 419 + 595, 217 + 433),
}

# Also need scroll down to get gm_mob and gm_pc since they are at y=824 and height is 900
for name, rect in boxes.items():
    crop = im.crop(rect)
    w, h = crop.size
    draw = ImageDraw.Draw(crop)
    for x_pct in range(0, 101, 10):
        x = int(w * x_pct / 100)
        draw.line([(x, 0), (x, h)], fill=(255, 255, 0, 120), width=1)
        draw.text((x + 2, 4), f"{x_pct}", fill=(255, 255, 0))
    for y_pct in range(0, 101, 10):
        y = int(h * y_pct / 100)
        draw.line([(0, y), (w, y)], fill=(255, 255, 0, 120), width=1)
        draw.text((4, y + 2), f"{y_pct}", fill=(255, 255, 0))
    crop.save(f"scratch/grid_{name}.jpg", quality=90)
    print(f"Saved scratch/grid_{name}.jpg")


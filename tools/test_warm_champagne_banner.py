import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Load Model 1
src_path = 'scratch/chosen_hero_models/model_1_solitaire_heart_yellow_dress.jpg'
img = Image.open(src_path).convert('RGB')
w, h = img.size

# --- A. MOBILE BANNER (768 x 1376) ---
target_aspect = 768 / 1376
crop_w = int(h * target_aspect)
crop_x0 = (w - crop_w) // 2
crop_box = (crop_x0, 0, crop_x0 + crop_w, h)
mob_img = img.crop(crop_box).resize((768, 1376), Image.Resampling.LANCZOS)

# Subtle warm color grade: warm highlights, glowing skin
mob_enh = ImageEnhance.Color(mob_img).enhance(1.08)
mob_enh = ImageEnhance.Contrast(mob_enh).enhance(1.05)
mob_enh = ImageEnhance.Sharpness(mob_enh).enhance(1.15)
mob_enh.save('scratch/hero_test/model_1_mobile_champagne.jpg', quality=95)

# --- B. DESKTOP BANNER (1376 x 768) ---
# Model height 768, preserve aspect ratio
model_h = 768
model_w = int(w * (model_h / h)) # approx 512px
model_resized = mob_enh.resize((model_w, model_h), Image.Resampling.LANCZOS)

# Background color of model at top-left edge
model_arr = np.array(model_resized)
edge_color = np.mean(model_arr[20:300, 0:30], axis=(0, 1)) # approx [215, 214, 215]
er, eg, eb = edge_color

# Solystra brand warm alabaster: #FAF8F5 -> (250, 248, 245)
# Create 1376x768 canvas with gradient from (250, 248, 245) on left to (er, eg, eb) at model seam
canvas_arr = np.zeros((768, 1376, 3), dtype=np.uint8)
seam_x = 1376 - model_w

for x in range(1376):
    if x <= seam_x:
        t = x / float(seam_x)
        # Gentle s-curve
        t_smooth = t * t * (3 - 2 * t)
        r = int(250 + t_smooth * (er - 250))
        g = int(248 + t_smooth * (eg - 248))
        b = int(245 + t_smooth * (eb - 245))
    else:
        r, g, b = int(er), int(eg), int(eb)
    canvas_arr[:, x, 0] = r
    canvas_arr[:, x, 1] = g
    canvas_arr[:, x, 2] = b

desktop_canvas = Image.fromarray(canvas_arr)

# Feathered paste of model
feather_px = 140
mask = np.ones((model_h, model_w), dtype=np.float32)
for col in range(feather_px):
    mask[:, col] = (col / float(feather_px)) ** 1.5

mask_img = Image.fromarray((mask * 255).astype(np.uint8))
desktop_canvas.paste(model_resized, (seam_x, 0), mask_img)

# Save
desktop_canvas.save('scratch/hero_test/model_1_desktop_champagne.jpg', quality=95)
print("Saved champagne hero test!")


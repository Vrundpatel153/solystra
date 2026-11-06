import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

src_path = 'scratch/chosen_hero_models/model_1_solitaire_heart_yellow_dress.jpg'
img = Image.open(src_path).convert('RGB')
w, h = img.size

# Convert to HSV or inspect pixels
arr = np.array(img, dtype=np.float32)
r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

# Saturation and brightness
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
sat = np.where(mx > 0, (mx - mn) / mx, 0)
val = mx

# The studio wall has low saturation (sat < 0.12) and high brightness (val > 150)
wall_mask = (sat < 0.12) & (val > 140)

# Smooth the mask to avoid harsh edges
wall_mask_img = Image.fromarray((wall_mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(15))
wall_mask_arr = np.array(wall_mask_img, dtype=np.float32) / 255.0

# Create luxury dark bronze-espresso studio wall: RGB (28, 22, 16) with subtle warm glow
target_bg = np.zeros_like(arr)
# Top-left darker (20, 16, 12), near model warm bronze glow (45, 34, 24)
for row in range(h):
    for col in range(w):
        factor = col / float(w)
        target_bg[row, col, 0] = 22 + factor * 25
        target_bg[row, col, 1] = 18 + factor * 20
        target_bg[row, col, 2] = 14 + factor * 16

# Blend wall with target_bg
enhanced_arr = arr * (1.0 - wall_mask_arr[:, :, None]) + target_bg * wall_mask_arr[:, :, None]
enhanced_img = Image.fromarray(np.clip(enhanced_arr, 0, 255).astype(np.uint8))

# Save enhanced vertical image
enhanced_img.save('scratch/hero_test/model_1_dark_luxury_mob.jpg', quality=95)

# --- Now Desktop Horizontal (1376 x 768) ---
model_h = 768
model_w = int(w * (model_h / h))
model_resized = enhanced_img.resize((model_w, model_h), Image.Resampling.LANCZOS)

# Create 1376x768 widescreen canvas with matching dark espresso gradient
pc_arr = np.zeros((768, 1376, 3), dtype=np.uint8)
for x in range(1376):
    factor = x / 1375.0
    pc_arr[:, x, 0] = int(18 + factor * 29)
    pc_arr[:, x, 1] = int(14 + factor * 24)
    pc_arr[:, x, 2] = int(10 + factor * 20)

desktop_canvas = Image.fromarray(pc_arr)

# Feather paste
feather_px = 160
mask = np.ones((model_h, model_w), dtype=np.float32)
for col in range(feather_px):
    mask[:, col] = (col / float(feather_px)) ** 1.3

mask_img = Image.fromarray((mask * 255).astype(np.uint8))
desktop_canvas.paste(model_resized, (1376 - model_w, 0), mask_img)

desktop_canvas.save('scratch/hero_test/model_1_dark_luxury_pc.jpg', quality=95)
print("Saved dark luxury test!")


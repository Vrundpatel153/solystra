import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

os.makedirs('scratch/hero_test', exist_ok=True)

# 1. Load Model 1 (DSC02715: 800x1200)
src_path = 'scratch/chosen_hero_models/model_1_solitaire_heart_yellow_dress.jpg'
img = Image.open(src_path).convert('RGB')
w, h = img.size

# --- A. MOBILE VERTICAL (768 x 1376) ---
# Target aspect ratio is 768 / 1376 = 0.558 (taller than 800/1200=0.667)
# Crop width to fit 9:16 ratio
target_aspect = 768 / 1376
crop_w = int(h * target_aspect)
crop_x0 = (w - crop_w) // 2
crop_box = (crop_x0, 0, crop_x0 + crop_w, h)
mob_crop = img.crop(crop_box).resize((768, 1376), Image.Resampling.LANCZOS)

# Enhance lighting: boost contrast, warm tint, slight sharpness
enhancer = ImageEnhance.Color(mob_crop)
mob_enhanced = enhancer.enhance(1.08)
enhancer = ImageEnhance.Contrast(mob_enhanced)
mob_enhanced = enhancer.enhance(1.06)
enhancer = ImageEnhance.Sharpness(mob_enhanced)
mob_enhanced = enhancer.enhance(1.12)

# Save mobile version
mob_enhanced.save('scratch/hero_test/model_1_mob_test.jpg', quality=92)

# --- B. DESKTOP HORIZONTAL (1376 x 768) ---
# Canvas is 1376 wide by 768 high.
# Model should occupy the right side (height 768, width ~512)
model_h = 768
model_w = int(w * (model_h / h))
model_resized = mob_enhanced.resize((model_w, model_h), Image.Resampling.LANCZOS)

# Create 1376x768 canvas with luxury bronze/espresso gradient
canvas = Image.new('RGB', (1376, 768), (28, 22, 16))
# Create horizontal gradient background: deep espresso (#18130E) on left to warm studio tone on right
grad = np.zeros((768, 1376, 3), dtype=np.uint8)
for x in range(1376):
    factor = x / 1375.0
    r = int(22 + factor * 24)
    g = int(18 + factor * 20)
    b = int(14 + factor * 16)
    grad[:, x, 0] = r
    grad[:, x, 1] = g
    grad[:, x, 2] = b

bg_img = Image.fromarray(grad)

# Paste model on the right with a soft feathered blend on the left edge
x_paste = 1376 - model_w
# Create soft linear alpha mask for smooth transition
mask = np.ones((model_h, model_w), dtype=np.float32)
feather_w = min(120, model_w // 3)
for col in range(feather_w):
    mask[:, col] = col / float(feather_w)

mask_img = Image.fromarray((mask * 255).astype(np.uint8))

bg_img.paste(model_resized, (x_paste, 0), mask_img)
bg_img.save('scratch/hero_test/model_1_pc_test.jpg', quality=92)

print("Model 1 test banners generated successfully!")


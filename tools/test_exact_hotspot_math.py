from PIL import Image, ImageDraw

# Let's write the exact mapping formula for object-cover:
def get_rendered_coords(orig_x, orig_y, container_w, container_h, obj_pos_x_pct, obj_pos_y_pct, orig_w=1024, orig_h=1536):
    scale = max(container_w / orig_w, container_h / orig_h)
    scaled_w = orig_w * scale
    scaled_h = orig_h * scale
    
    max_crop_x = scaled_w - container_w
    max_crop_y = scaled_h - container_h
    
    crop_x = max_crop_x * (obj_pos_x_pct / 100.0)
    crop_y = max_crop_y * (obj_pos_y_pct / 100.0)
    
    rendered_x = orig_x * scale - crop_x
    rendered_y = orig_y * scale - crop_y
    
    pct_x = (rendered_x / container_w) * 100.0
    pct_y = (rendered_y / container_h) * 100.0
    
    return pct_x, pct_y

# Original landmarks:
# C2 (second_combo.png):
# Earring: x = 670, y = 575
# Necklace: x = 444, y = 1136
# GM (golden_meadow_set_combo.png):
# Choker / Necklace: x = 440, y = 1140 (central drop) or flower x = 330, y = 1030

# Let's test with:
# Mobile: 358 x 460, obj_pos: center 40% (x=50%, y=40%)
# Desktop: lg:col-span-5 or lg:col-span-6.
# If grid is 12 columns, max-w-7xl (1280px), px-8 (64px) -> 1216px total.
# If col-span-5: width = 1216 * 5/12 - gap = 485px.
# If col-span-6: width = (1216 - 32) / 2 = 592px.
# With height = 580px:
# Aspect ratio = 592 / 580 = 1.02.
# obj_pos: center 40% (x=50%, y=40%)

print("=== COMBO 1 (C2) ===")
# Mobile (358 x 460)
mob_c2_ear_x, mob_c2_ear_y = get_rendered_coords(670, 575, 358, 460, 50, 40)
mob_c2_neck_x, mob_c2_neck_y = get_rendered_coords(444, 1136, 358, 460, 50, 40)
print(f"Mobile (358x460): Earring = {mob_c2_ear_x:.1f}%, {mob_c2_ear_y:.1f}% | Necklace = {mob_c2_neck_x:.1f}%, {mob_c2_neck_y:.1f}%")

# Desktop (592 x 580)
pc_c2_ear_x, pc_c2_ear_y = get_rendered_coords(670, 575, 592, 580, 50, 40)
pc_c2_neck_x, pc_c2_neck_y = get_rendered_coords(444, 1136, 592, 580, 50, 40)
print(f"Desktop (592x580): Earring = {pc_c2_ear_x:.1f}%, {pc_c2_ear_y:.1f}% | Necklace = {pc_c2_neck_x:.1f}%, {pc_c2_neck_y:.1f}%")

print("\n=== COMBO 2 (GM) ===")
# Mobile (358 x 460)
mob_gm_neck_x, mob_gm_neck_y = get_rendered_coords(440, 1140, 358, 460, 50, 40)
print(f"Mobile (358x460): Choker = {mob_gm_neck_x:.1f}%, {mob_gm_neck_y:.1f}%")

# Desktop (592 x 580)
pc_gm_neck_x, pc_gm_neck_y = get_rendered_coords(440, 1140, 592, 580, 50, 40)
print(f"Desktop (592x580): Choker = {pc_gm_neck_x:.1f}%, {pc_gm_neck_y:.1f}%")


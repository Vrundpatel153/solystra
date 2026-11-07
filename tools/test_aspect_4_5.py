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

# Test with 480 x 600 (aspect 4:5):
print("--- 480 x 600 (aspect 4:5) ---")
c2_ear_x, c2_ear_y = get_rendered_coords(670, 575, 480, 600, 50, 40)
c2_neck_x, c2_neck_y = get_rendered_coords(444, 1136, 480, 600, 50, 40)
print(f"C2: Earring = {c2_ear_x:.1f}%, {c2_ear_y:.1f}% | Necklace = {c2_neck_x:.1f}%, {c2_neck_y:.1f}%")

gm_neck_x, gm_neck_y = get_rendered_coords(440, 1140, 480, 600, 50, 40)
print(f"GM: Choker = {gm_neck_x:.1f}%, {gm_neck_y:.1f}%")

# Test with 450 x 600 (aspect 3:4):
print("\n--- 450 x 600 (aspect 3:4) ---")
c2_ear_x, c2_ear_y = get_rendered_coords(670, 575, 450, 600, 50, 40)
c2_neck_x, c2_neck_y = get_rendered_coords(444, 1136, 450, 600, 50, 40)
print(f"C2: Earring = {c2_ear_x:.1f}%, {c2_ear_y:.1f}% | Necklace = {c2_neck_x:.1f}%, {c2_neck_y:.1f}%")

gm_neck_x, gm_neck_y = get_rendered_coords(440, 1140, 450, 600, 50, 40)
print(f"GM: Choker = {gm_neck_x:.1f}%, {gm_neck_y:.1f}%")

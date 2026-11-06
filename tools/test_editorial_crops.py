import os
from PIL import Image

src_dir = 'scratch/curated_highres'
out_dir = 'scratch/test_crops'
os.makedirs(out_dir, exist_ok=True)

models = [
    ('hero_1', 'hero_1_heart_yellow_DSC02721.jpg', (0.5, 0.35)), # center on face & necklace
    ('hero_2', 'hero_2_pearl_blazer_DSC02810.jpg', (0.5, 0.35)), # center on face & necklace
    ('hero_3', 'hero_3_tennis_green_DSC02915.jpg', (0.5, 0.40)), # center on face, wrist & bracelet
    ('hero_4', 'hero_4_tiara_blazer_DSC02831.jpg', (0.5, 0.35)), # center on face & tiara
]

print("Testing crops for desktop (1376x768) and mobile (768x1376)...")

for mid, fname, (fx, fy) in models:
    p = os.path.join(src_dir, fname)
    with Image.open(p) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        
        # 1. MOBILE 9:16 (768x1376)
        mob_aspect = 768 / 1376.0
        mob_w = int(h * mob_aspect)
        if mob_w > w:
            mob_w = w
            mob_h = int(w / mob_aspect)
        else:
            mob_h = h
        
        mx0 = max(0, min(w - mob_w, int(w * fx) - mob_w // 2))
        my0 = max(0, min(h - mob_h, int(h * fy) - mob_h // 2))
        mob_crop = rgb.crop((mx0, my0, mx0 + mob_w, my0 + mob_h)).resize((768, 1376), Image.Resampling.LANCZOS)
        mob_crop.save(os.path.join(out_dir, f"{mid}_mob.jpg"), quality=90)
        
        # 2. DESKTOP 16:9 (1376x768)
        pc_aspect = 1376 / 768.0
        pc_h = int(w / pc_aspect)
        if pc_h > h:
            pc_h = h
            pc_w = int(h * pc_aspect)
        else:
            pc_w = w
        
        px0 = max(0, min(w - pc_w, int(w * fx) - pc_w // 2))
        py0 = max(0, min(h - pc_h, int(h * fy) - pc_h // 2))
        pc_crop = rgb.crop((px0, py0, px0 + pc_w, py0 + pc_h)).resize((1376, 768), Image.Resampling.LANCZOS)
        pc_crop.save(os.path.join(out_dir, f"{mid}_pc.jpg"), quality=90)
        
        print(f"Saved {mid}_mob (768x1376) and {mid}_pc (1376x768)")

print("Crops complete.")

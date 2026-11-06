import os
from PIL import Image, ImageEnhance

targets = [
    'jewellery-design-html/solystra_assets/banners',
    'jewellery-design-html-dist/solystra_assets/banners',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\banners',
    'public/solystra_assets/banners'
]

for t in targets:
    os.makedirs(t, exist_ok=True)

models = [
    {
        'id': 'hero_model_1',
        'src': 'scratch/curated_highres/hero_1_heart_yellow_DSC02721.jpg',
        'crop_y': 0.25, # Upper half focusing on face & heart pendant
    },
    {
        'id': 'hero_model_2',
        'src': 'scratch/curated_highres/hero_2_pearl_blazer_DSC02810.jpg',
        'crop_y': 0.28, # Upper half focusing on face & layered pearl necklace
    },
    {
        'id': 'hero_model_3',
        'src': 'scratch/curated_highres/hero_3_tennis_green_DSC02915.jpg',
        'crop_y': 0.32, # Focus on face, wrist & tennis bracelet
    },
    {
        'id': 'hero_model_4',
        'src': 'scratch/curated_highres/hero_4_tiara_blazer_DSC02831.jpg',
        'crop_y': 0.26, # Focus on face & tiara pendant
    },
]

print("Processing authentic high-res hero banners (PC: 1200x800, Mob: 800x1200)...")

for m in models:
    mid = m['id']
    src = m['src']
    with Image.open(src) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        
        # 1. PC Split Column Image (Aspect 3:2 or 4:3, e.g. 1200x800)
        # Crop focusing naturally on model and jewelry
        pc_aspect = 1.35 # slightly taller than 16:9 for the right column
        target_w = w
        target_h = int(w / pc_aspect)
        if target_h > h:
            target_h = h
            target_w = int(h * pc_aspect)
        
        cy = int(h * m['crop_y'])
        y0 = max(0, min(h - target_h, cy - target_h // 2))
        x0 = max(0, min(w - target_w, (w - target_w) // 2))
        
        pc_cropped = rgb.crop((x0, y0, x0 + target_w, y0 + target_h)).resize((1200, 888), Image.Resampling.LANCZOS)
        pc_enh = ImageEnhance.Sharpness(pc_cropped).enhance(1.12)
        pc_enh = ImageEnhance.Contrast(pc_enh).enhance(1.04)
        
        # 2. Mobile Full Portrait (800x1200, aspect 2:3)
        mob_aspect = 2.0 / 3.0
        mob_w = int(h * mob_aspect)
        if mob_w > w:
            mob_w = w
            mob_h = int(w / mob_aspect)
        else:
            mob_h = h
            
        my0 = max(0, min(h - mob_h, int(h * 0.28) - mob_h // 2))
        mx0 = max(0, min(w - mob_w, (w - mob_w) // 2))
        
        mob_cropped = rgb.crop((mx0, my0, mx0 + mob_w, my0 + mob_h)).resize((800, 1200), Image.Resampling.LANCZOS)
        mob_enh = ImageEnhance.Sharpness(mob_cropped).enhance(1.12)
        mob_enh = ImageEnhance.Contrast(mob_enh).enhance(1.04)
        
        for d in targets:
            pc_enh.save(os.path.join(d, f"{mid}_pc.webp"), format='WEBP', quality=90, method=6)
            pc_enh.save(os.path.join(d, f"{mid}_pc.jpg"), format='JPEG', quality=92)
            mob_enh.save(os.path.join(d, f"{mid}_mob.webp"), format='WEBP', quality=90, method=6)
            mob_enh.save(os.path.join(d, f"{mid}_mob.jpg"), format='JPEG', quality=92)
            
        print(f"Saved {mid}_pc (1200x888) and {mid}_mob (800x1200)")

print("All hero banners successfully generated and saved to all target directories.")


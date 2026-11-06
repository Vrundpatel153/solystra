import os
import sys
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

target_dirs = [
    'jewellery-design-html/solystra_assets/banners',
    'jewellery-design-html-dist/solystra_assets/banners',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\banners',
    'public/solystra_assets/banners',
]

for d in target_dirs:
    os.makedirs(d, exist_ok=True)

# 4 Authentic Hero Slides with genuine model & jewelry match
slides = [
    {
        'id': 'hero_model_1',
        'title': 'The Solitaire Heart Suite',
        'src': 'scratch/chosen_hero_models/model_1_solitaire_heart_yellow_dress.jpg',
        'crop_y1': 40,
        'crop_y2': 1180,
    },
    {
        'id': 'hero_model_2',
        'title': 'Layered Pearl Solitaire',
        'src': 'scratch/model_candidates/DSC02724.JPG',
        'crop_y1': 0,
        'crop_y2': 1180,
    },
    {
        'id': 'hero_model_3',
        'title': 'Austrian Tennis Bracelet',
        'src': 'scratch/model_candidates/DSC02822.JPG',
        'crop_y1': 0,
        'crop_y2': 1180,
    },
    {
        'id': 'hero_model_4',
        'title': 'The Royal Tiara Solitaire',
        'src': 'scratch/model_candidates/DSC02745.JPG',
        'crop_y1': 0,
        'crop_y2': 1180,
    },
]

print("Building Art-Directed Master Hero Banners for Solystra Jewels...")

for s in slides:
    mid = s['id']
    src_path = s['src']
    
    with Image.open(src_path) as im:
        raw_rgb = im.convert('RGB')
        w, h = raw_rgb.size
        
        # -------------------------------------------------------------
        # 1. DESKTOP SPLIT COLUMN IMAGE (900 x 600, aspect 1.5:1)
        # The right column is ~56% width, 520px high.
        # We want the model to comfortably fill the right column,
        # with her full head, hair, eyes, smile, and jewelry framed perfectly.
        # -------------------------------------------------------------
        y1 = s['crop_y1']
        y2 = min(h, s['crop_y2'])
        model_crop = raw_rgb.crop((0, y1, w, y2))
        
        # Scale model crop to fill 900px height (True Window Height for Desktop)
        target_h = 900
        target_w = int(w * (target_h / float(y2 - y1))) # ~610px
        model_scaled = model_crop.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # The right column is ~56% width (~807px on a 1440 screen) and 792-900px high.
        # We place model on an 850x900 canvas, perfectly matching the right column!
        canvas_w, canvas_h = 850, 900
        pc_canvas = Image.new('RGB', (canvas_w, canvas_h), color=(20, 18, 16))
        
        # Position model from right edge:
        paste_x = canvas_w - target_w # ~240px
        pc_canvas.paste(model_scaled, (paste_x, 0))
        
        # Sample average color of model's left studio background
        model_arr = np.array(model_scaled)
        sample_left = model_arr[:, :20, :]
        mean_left_bg = np.mean(sample_left, axis=(0, 1))
        
        # Create an ultra-smooth luxury gradient extending from x=0 (#141210) to paste_x
        canvas_arr = np.array(pc_canvas, dtype=np.float32)
        noir_bg = np.array([20, 18, 16], dtype=np.float32)
        
        # Blend from x=0 (noir) to paste_x + 80px (model)
        fade_end = paste_x + 80
        for x in range(fade_end):
            if x < paste_x:
                t = float(x) / float(paste_x)
                # smoothstep
                t = t * t * (3.0 - 2.0 * t)
                canvas_arr[:, x, :] = noir_bg * (1.0 - t) + mean_left_bg * t
            else:
                # feather into the model's actual pixels
                feather_t = float(x - paste_x) / 80.0
                feather_t = feather_t * feather_t * (3.0 - 2.0 * feather_t)
                orig_pixels = canvas_arr[:, x, :]
                canvas_arr[:, x, :] = mean_left_bg * (1.0 - feather_t) + orig_pixels * feather_t
                
        pc_final = Image.fromarray(np.clip(canvas_arr, 0, 255).astype(np.uint8))
        pc_final = ImageEnhance.Sharpness(pc_final).enhance(1.10)
        pc_final = ImageEnhance.Contrast(pc_final).enhance(1.02)
        
        # -------------------------------------------------------------
        # 2. MOBILE FULL-PORTRAIT HERO (800 x 1200, aspect 2:3)
        # Framed from top of hair so her head, eyes, smile, and jewelry
        # are in the upper 65% of the mobile screen.
        # -------------------------------------------------------------
        mob_crop = raw_rgb.crop((0, 0, w, int(h * 0.95)))
        mob_final = mob_crop.resize((800, 1200), Image.Resampling.LANCZOS)
        mob_final = ImageEnhance.Sharpness(mob_final).enhance(1.10)
        mob_final = ImageEnhance.Contrast(mob_final).enhance(1.02)
        
        for d in target_dirs:
            pc_final.save(os.path.join(d, f"{mid}_pc.webp"), format='WEBP', quality=92, method=6)
            pc_final.save(os.path.join(d, f"{mid}_pc.jpg"), format='JPEG', quality=92)
            mob_final.save(os.path.join(d, f"{mid}_mob.webp"), format='WEBP', quality=92, method=6)
            mob_final.save(os.path.join(d, f"{mid}_mob.jpg"), format='JPEG', quality=92)
            
        print(f"✓ Generated {mid}: Desktop (900x600) & Mobile (800x1200) for '{s['title']}'")

print("All master hero banners successfully generated and saved!")

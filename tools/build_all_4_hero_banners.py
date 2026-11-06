import os
import gc
from PIL import Image, ImageEnhance
import numpy as np

target_dirs = [
    'jewellery-design-html/solystra_assets/banners',
    'jewellery-design-html-dist/solystra_assets/banners',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\banners',
    'public/solystra_assets/banners',
]

for d in target_dirs:
    os.makedirs(d, exist_ok=True)

models = [
    {
        'id': 'hero_model_1',
        'src': 'scratch/chosen_hero_models/model_1_solitaire_heart_yellow_dress.jpg',
        'name': 'Solitaire Heart Necklace in Yellow Dress',
        'crop_shift_x': 0,
    },
    {
        'id': 'hero_model_2',
        'src': 'scratch/chosen_hero_models/model_2_pearl_solitaire_blazer.jpg',
        'name': 'Layered Pearl and Diamond Solitaire in Black Blazer',
        'crop_shift_x': 0,
    },
    {
        'id': 'hero_model_3',
        'src': 'scratch/chosen_hero_models/model_3_crown_tiara_blazer.jpg',
        'name': 'Royal Crown Tiara Solitaire in Black Blazer',
        'crop_shift_x': 0,
    },
    {
        'id': 'hero_model_4',
        'src': 'scratch/chosen_hero_models/model_4_tennis_bracelet_green_dress.jpg',
        'name': 'Diamond Tennis Bracelet in Sage Green Dress',
        'crop_shift_x': 0,
    },
]

print(f"Processing {len(models)} models into mobile (768x1376) and desktop (1376x768) hero banners...")

for m in models:
    mid = m['id']
    src = m['src']
    print(f"\nProcessing {mid} ({m['name']})...")
    
    with Image.open(src) as raw_img:
        img = raw_img.convert('RGB')
        w, h = img.size

        # --- A. MOBILE VERTICAL (768 x 1376) ---
        target_aspect = 768 / 1376
        crop_w = int(h * target_aspect)
        crop_x0 = max(0, min(w - crop_w, (w - crop_w) // 2 + m['crop_shift_x']))
        crop_box = (crop_x0, 0, crop_x0 + crop_w, h)
        mob_img = img.crop(crop_box).resize((768, 1376), Image.Resampling.LANCZOS)

        # Enhance lighting
        mob_enh = ImageEnhance.Color(mob_img).enhance(1.08)
        mob_enh = ImageEnhance.Contrast(mob_enh).enhance(1.05)
        mob_enh = ImageEnhance.Sharpness(mob_enh).enhance(1.15)
        del mob_img

        # Save mobile version in all target directories
        for d in target_dirs:
            mob_enh.save(os.path.join(d, f'{mid}_mob.webp'), format='WEBP', quality=90, method=6)
            mob_enh.save(os.path.join(d, f'{mid}_mob.jpg'), format='JPEG', quality=92)
        print(f"  Saved {mid}_mob (768x1376)")

        # --- B. DESKTOP HORIZONTAL (1376 x 768) ---
        model_h = 768
        model_w = int(w * (model_h / h)) # approx 512px
        model_resized = mob_enh.resize((model_w, model_h), Image.Resampling.LANCZOS)
        del mob_enh

        # Sample background edge color
        model_arr = np.array(model_resized)
        edge_color = np.mean(model_arr[20:300, 0:30], axis=(0, 1))
        er, eg, eb = edge_color

        # Create 1376x768 canvas with gradient from #FAF8F5 (250, 248, 245) to edge_color
        canvas_arr = np.zeros((768, 1376, 3), dtype=np.uint8)
        seam_x = 1376 - model_w

        for x in range(1376):
            if x <= seam_x:
                t = x / float(seam_x)
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
        del canvas_arr

        # Feathered paste of model
        feather_px = 140
        mask = np.ones((model_h, model_w), dtype=np.float32)
        for col in range(feather_px):
            mask[:, col] = (col / float(feather_px)) ** 1.5

        mask_img = Image.fromarray((mask * 255).astype(np.uint8))
        desktop_canvas.paste(model_resized, (seam_x, 0), mask_img)
        del mask, mask_img, model_resized, model_arr

        # Save desktop version in all target directories
        for d in target_dirs:
            desktop_canvas.save(os.path.join(d, f'{mid}_pc.webp'), format='WEBP', quality=90, method=6)
            desktop_canvas.save(os.path.join(d, f'{mid}_pc.jpg'), format='JPEG', quality=92)
        print(f"  Saved {mid}_pc (1376x768)")
        del desktop_canvas

    gc.collect()

print("\nAll 4 hero models successfully generated in both mobile and desktop formats!")


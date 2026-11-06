import os
import sys
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

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
        'title': 'The Solitaire Heart Suite',
        'tag': 'ATELIER SIGNATURE',
        'desc': 'Pure 925 sterling silver with sparkling Austrian solitaire heart pendant.',
        'button': 'Explore Necklaces',
        'href': 'products.html?category=necklaces'
    },
    {
        'id': 'hero_model_2',
        'src': 'scratch/chosen_hero_models/model_2_pearl_solitaire_blazer.jpg',
        'title': 'Modern Classics Collection',
        'tag': 'MOST LOVED',
        'desc': 'Double-layered solitaire diamond and natural freshwater pearl necklace.',
        'button': 'Shop Collection',
        'href': 'products.html?category=complete-sets'
    },
    {
        'id': 'hero_model_3',
        'src': 'scratch/chosen_hero_models/model_3_crown_tiara_blazer.jpg',
        'title': 'Royal Crown Solitaire',
        'tag': 'NEW ARRIVALS',
        'desc': 'Bespoke tiara-cut dancing solitaire in handcrafted 925 sterling silver.',
        'button': 'View Solitaires',
        'href': 'products.html?category=necklaces'
    },
    {
        'id': 'hero_model_4',
        'src': 'scratch/chosen_hero_models/model_4_tennis_bracelet_green_dress.jpg',
        'title': 'Austrian Tennis Bracelet',
        'tag': 'ICONIC SILHOUETTE',
        'desc': 'Continuous hand-set Austrian solitaires in 18K Italian gold vermeil & 925 silver.',
        'button': 'Discover Bracelets',
        'href': 'products.html?category=bracelets'
    },
]

print("Starting generation of all 4 hero banners (Mobile & PC)...")

for m in models:
    mid = m['id']
    src = m['src']
    print(f"\nProcessing {mid}: {m['title']}...")
    
    with Image.open(src) as raw_img:
        img = raw_img.convert('RGB')
        w, h = img.size
        
        # 1. Color and light enhancement (gentle, keeping authentic model look)
        enh = ImageEnhance.Color(img).enhance(1.06)
        enh = ImageEnhance.Contrast(enh).enhance(1.05)
        enh = ImageEnhance.Sharpness(enh).enhance(1.12)
        
        # --- A. MOBILE BANNER (768 x 1376, 9:16 ratio) ---
        target_aspect = 768 / 1376
        crop_w = int(h * target_aspect)
        crop_x0 = max(0, min(w - crop_w, (w - crop_w) // 2))
        crop_box = (crop_x0, 0, crop_x0 + crop_w, h)
        mob_img = enh.crop(crop_box).resize((768, 1376), Image.Resampling.LANCZOS)
        
        # Save mobile version
        for d in target_dirs:
            mob_img.save(os.path.join(d, f'{mid}_mob.webp'), format='WEBP', quality=90, method=6)
            mob_img.save(os.path.join(d, f'{mid}_mob.jpg'), format='JPEG', quality=92)
        print(f"  Saved {mid}_mob (768x1376)")
        
        # --- B. DESKTOP WIDESCREEN BANNER (1376 x 768, 16:9 ratio) ---
        # Scale model so height is 768px
        model_h = 768
        model_w = int(w * (model_h / float(h))) # ~512px
        model_scaled = enh.resize((model_w, model_h), Image.Resampling.LANCZOS)
        
        # We place model on the right half: right aligned
        seam_x = 1376 - model_w # ~864px
        
        # Create dark luxury background: deep espresso/bronze tone
        # Smooth gradient: Left side (x=0) is (22, 17, 13) deep rich espresso
        # Right side blends into model's studio wall tone
        model_arr = np.array(model_scaled, dtype=np.float32)
        # Sample edge color on the left of the model image
        edge_col = np.mean(model_arr[20:300, 0:30], axis=(0, 1)) # typically grey ~210
        
        canvas_arr = np.zeros((768, 1376, 3), dtype=np.float32)
        
        # Fill base background with dark luxury studio gradient
        for col_idx in range(1376):
            factor = col_idx / 1375.0
            # Warm dark espresso to deep bronze
            canvas_arr[:, col_idx, 0] = 20.0 + factor * 22.0
            canvas_arr[:, col_idx, 1] = 16.0 + factor * 17.0
            canvas_arr[:, col_idx, 2] = 12.0 + factor * 12.0
            
        # Feather width for seamless blend (200px)
        feather_w = min(220, model_w // 2)
        alpha_mask = np.ones((model_h, model_w), dtype=np.float32)
        for col_i in range(feather_w):
            t = col_i / float(feather_w)
            # Smooth cubic curve
            alpha_mask[:, col_i] = t * t * (3.0 - 2.0 * t)
            
        # Composite model onto canvas
        desktop_canvas = Image.fromarray(np.clip(canvas_arr, 0, 255).astype(np.uint8))
        mask_pil = Image.fromarray((alpha_mask * 255).astype(np.uint8))
        
        desktop_canvas.paste(model_scaled, (seam_x, 0), mask_pil)
        
        # Save desktop version
        for d in target_dirs:
            desktop_canvas.save(os.path.join(d, f'{mid}_pc.webp'), format='WEBP', quality=90, method=6)
            desktop_canvas.save(os.path.join(d, f'{mid}_pc.jpg'), format='JPEG', quality=92)
        print(f"  Saved {mid}_pc (1376x768)")

print("\nAll 4 Hero Model Banners successfully produced!")


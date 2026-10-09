import os
import shutil
from PIL import Image
import numpy as np

# Target color: HEX #145C59, RGB (20, 92, 89)
# HSL: 177 deg, 64%, 22%
TARGET_HUE = 177.0 / 360.0  # 0.491666...
TARGET_SAT = 0.64
TARGET_VAL_RATIO = 92.0 / 122.0  # ratio of primary channel

def recolor_image(im_path):
    """
    Recolors red/maroon/burgundy tones in an image to deep luxury emerald-teal #145C59
    while maintaining specular highlights, gold tones, and textures.
    """
    im = Image.open(im_path).convert('RGB')
    arr = np.array(im, dtype=np.float32) / 255.0
    
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    
    maxc = np.maximum(np.maximum(r, g), b)
    minc = np.minimum(np.minimum(r, g), b)
    delta = maxc - minc
    
    s = np.zeros_like(maxc)
    mask = maxc > 1e-5
    s[mask] = delta[mask] / maxc[mask]
    
    h = np.zeros_like(maxc)
    d_mask = delta > 1e-5
    
    rc = np.zeros_like(maxc)
    gc = np.zeros_like(maxc)
    bc = np.zeros_like(maxc)
    rc[d_mask] = (maxc[d_mask] - r[d_mask]) / delta[d_mask]
    gc[d_mask] = (maxc[d_mask] - g[d_mask]) / delta[d_mask]
    bc[d_mask] = (maxc[d_mask] - b[d_mask]) / delta[d_mask]
    
    mask_r = d_mask & (r == maxc)
    h[mask_r] = (bc[mask_r] - gc[mask_r]) % 6.0
    
    mask_g = d_mask & (g == maxc) & (~mask_r)
    h[mask_g] = 2.0 + rc[mask_g] - bc[mask_g]
    
    mask_b = d_mask & (b == maxc) & (~mask_r) & (~mask_g)
    h[mask_b] = 4.0 + gc[mask_b] - rc[mask_b]
    
    h = (h / 6.0) % 1.0
    v = maxc
    
    # Calculate distance to red/maroon hue (around 350-0-15 degrees)
    dist_0 = np.abs(h - 0.0)
    dist_1 = np.abs(h - 1.0)
    dist_350 = np.abs(h - 0.97)
    min_dist = np.minimum(np.minimum(dist_0, dist_1), dist_350)
    
    # Weight for red tones:
    # Must be close to red hue, have sufficient saturation, and be distinct from yellow/gold (h > 0.09)
    hue_factor = np.clip((0.15 - min_dist) / 0.15, 0.0, 1.0)
    sat_factor = np.clip((s - 0.08) / 0.12, 0.0, 1.0)
    
    # Exclude warm gold / brass metals where g is high relative to r (g/r > 0.65 when bright)
    gold_mask = (r > 0.4) & (g > 0.28) & (b < g) & (g / np.maximum(r, 1e-4) > 0.68)
    not_gold = 1.0 - np.clip(gold_mask.astype(np.float32) * 1.5, 0.0, 1.0)
    
    weight = hue_factor * sat_factor * not_gold
    
    # Smooth weight curves
    weight = weight * weight * (3.0 - 2.0 * weight)
    
    # Calculate new HSV
    new_h = (1.0 - weight) * h + weight * TARGET_HUE
    new_s = (1.0 - weight) * s + weight * np.clip(s * 1.05, 0.50, 0.85)
    
    # Retain natural shadow depth & luminance matching #145C59
    # In #145C59 (20, 92, 89), V is around 0.36 for the base color, with deep shadows down to 0.08
    new_v = (1.0 - weight) * v + weight * (v * 0.95)
    
    # Vectorized HSV to RGB
    hi = np.floor(new_h * 6.0).astype(int) % 6
    f = (new_h * 6.0) - np.floor(new_h * 6.0)
    p = new_v * (1.0 - new_s)
    q = new_v * (1.0 - f * new_s)
    t = new_v * (1.0 - (1.0 - f) * new_s)
    
    out_r = np.zeros_like(new_v)
    out_g = np.zeros_like(new_v)
    out_b = np.zeros_like(new_v)
    
    idx = hi == 0
    out_r[idx], out_g[idx], out_b[idx] = new_v[idx], t[idx], p[idx]
    idx = hi == 1
    out_r[idx], out_g[idx], out_b[idx] = q[idx], new_v[idx], p[idx]
    idx = hi == 2
    out_r[idx], out_g[idx], out_b[idx] = p[idx], new_v[idx], t[idx]
    idx = hi == 3
    out_r[idx], out_g[idx], out_b[idx] = p[idx], q[idx], new_v[idx]
    idx = hi == 4
    out_r[idx], out_g[idx], out_b[idx] = t[idx], p[idx], new_v[idx]
    idx = hi == 5
    out_r[idx], out_g[idx], out_b[idx] = new_v[idx], p[idx], q[idx]
    
    out_arr = np.clip(np.stack([out_r, out_g, out_b], axis=2) * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(out_arr)

def process_file_bundle(base_path_no_ext, formats=['png', 'jpg', 'webp']):
    """
    Finds the master image for base_path_no_ext, transforms it, and saves all requested formats.
    """
    master = None
    for ext in ['png', 'jpg', 'jpeg', 'webp']:
        candidate = f"{base_path_no_ext}.{ext}"
        if os.path.exists(candidate):
            master = candidate
            break
            
    if not master:
        print(f"Warning: Master image not found for {base_path_no_ext}")
        return
        
    print(f"Transforming master: {master}")
    recolored = recolor_image(master)
    
    for ext in formats:
        target = f"{base_path_no_ext}.{ext}"
        if ext == 'png':
            recolored.save(target, 'PNG', optimize=True)
        elif ext in ['jpg', 'jpeg']:
            recolored.save(target, 'JPEG', quality=95)
        elif ext == 'webp':
            recolored.save(target, 'WEBP', quality=95)
        print(f"  -> Generated {target}")

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # 1. Category cards in solystra_assets/categories/zavya_style/
    cat_items = ['anklets', 'bracelets', 'complete_sets', 'earrings', 'necklaces', 'rings']
    for cat in cat_items:
        base = os.path.join(root, 'solystra_assets', 'categories', 'zavya_style', cat)
        process_file_bundle(base, ['png', 'jpg', 'webp'])
        
    # 2. Promos
    promos = [
        'atelier_luxury_banner',
        'bogo_gift_solitaire',
        'bogo_privilege_bg'
    ]
    for p in promos:
        base = os.path.join(root, 'solystra_assets', 'promos', p)
        process_file_bundle(base, ['jpg', 'webp'])
        
    # 3. Banners
    banners = [
        'banner_pc_1',
        'banner_mob_1',
        'bogo_privilege_bg',
        'offers_privilege_vault_banner'
    ]
    for b in banners:
        base = os.path.join(root, 'solystra_assets', 'banners', b)
        process_file_bundle(base, ['jpg', 'webp'])

    print("\nImage transformation complete! Now syncing to public, jewellery-design-html, and dist...")
    
    # Sync folders
    sync_sources = [
        ('solystra_assets/categories/zavya_style', 'public/solystra_assets/categories/zavya_style'),
        ('solystra_assets/categories/zavya_style', 'jewellery-design-html/solystra_assets/categories/zavya_style'),
        ('solystra_assets/categories/zavya_style', 'jewellery-design-html-dist/solystra_assets/categories/zavya_style'),
        
        ('solystra_assets/promos', 'public/solystra_assets/promos'),
        ('solystra_assets/promos', 'jewellery-design-html/solystra_assets/promos'),
        ('solystra_assets/promos', 'jewellery-design-html-dist/solystra_assets/promos'),
        
        ('solystra_assets/banners', 'public/solystra_assets/banners'),
        ('solystra_assets/banners', 'jewellery-design-html/solystra_assets/banners'),
        ('solystra_assets/banners', 'jewellery-design-html-dist/solystra_assets/banners'),
    ]
    
    for s_rel, d_rel in sync_sources:
        s_abs = os.path.join(root, s_rel)
        d_abs = os.path.join(root, d_rel)
        if os.path.exists(s_abs):
            os.makedirs(d_abs, exist_ok=True)
            for f in os.listdir(s_abs):
                s_f = os.path.join(s_abs, f)
                d_f = os.path.join(d_abs, f)
                if os.path.isfile(s_f):
                    shutil.copy2(s_f, d_f)
            print(f"Synced {s_rel} -> {d_rel}")

if __name__ == '__main__':
    main()

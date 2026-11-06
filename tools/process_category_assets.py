import os
from PIL import Image, ImageEnhance

targets = [
    'jewellery-design-html/solystra_assets/categories/zavya_style',
    'jewellery-design-html-dist/solystra_assets/categories/zavya_style',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\categories\zavya_style',
    'public/solystra_assets/categories/zavya_style'
]

for t in targets:
    os.makedirs(t, exist_ok=True)

mapping = {
    'necklaces.webp': ('scratch/curated_highres/cat_necklaces_DSC03100.jpg', (0.5, 0.5)),
    'rings.webp': ('scratch/curated_highres/cat_rings_DSC03013.jpg', (0.55, 0.5)),
    'bracelets.webp': ('scratch/curated_highres/cat_bracelets_DSC03087.jpg', (0.5, 0.5)),
    'earrings.webp': ('scratch/curated_highres/cat_earrings_DSC03001.jpg', (0.5, 0.5)),
    'anklets.webp': ('scratch/curated_highres/cat_anklets_DSC03040.jpg', (0.5, 0.45)),
    'sets.webp': ('scratch/curated_highres/cat_suites_DSC03045.jpg', (0.5, 0.5)),
}

print("Processing category images to 600x600 WebP...")

for out_name, (src_file, (fx, fy)) in mapping.items():
    with Image.open(src_file) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        # Make a square crop of size min(w, h) centered at (fx, fy)
        side = min(w, h)
        cx = int(w * fx)
        cy = int(h * fy)
        
        x0 = max(0, min(w - side, cx - side // 2))
        y0 = max(0, min(h - side, cy - side // 2))
        
        cropped = rgb.crop((x0, y0, x0 + side, y0 + side))
        resized = cropped.resize((600, 600), Image.Resampling.LANCZOS)
        
        # Subtle luxury enhancement
        enh = ImageEnhance.Sharpness(resized).enhance(1.15)
        enh = ImageEnhance.Contrast(enh).enhance(1.04)
        
        for t in targets:
            out_path = os.path.join(t, out_name)
            enh.save(out_path, format='WEBP', quality=90, method=6)
            
        print(f"Saved {out_name} (600x600)")

print("All category images processed and deployed to all target directories.")

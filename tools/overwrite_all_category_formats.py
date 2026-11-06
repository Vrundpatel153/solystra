import os
from PIL import Image, ImageEnhance

targets = [
    'jewellery-design-html/solystra_assets/categories/zavya_style',
    'jewellery-design-html-dist/solystra_assets/categories/zavya_style',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\categories\zavya_style',
    'public/solystra_assets/categories/zavya_style'
]

mapping = {
    'necklaces': ('scratch/curated_highres/cat_necklaces_DSC03100.jpg', (0.5, 0.5)),
    'rings': ('scratch/curated_highres/cat_rings_DSC03013.jpg', (0.55, 0.5)),
    'bracelets': ('scratch/curated_highres/cat_bracelets_DSC03087.jpg', (0.5, 0.5)),
    'earrings': ('scratch/curated_highres/cat_earrings_DSC03001.jpg', (0.5, 0.5)),
    'anklets': ('scratch/curated_highres/cat_anklets_DSC03040.jpg', (0.5, 0.45)),
    'sets': ('scratch/curated_highres/cat_suites_DSC03045.jpg', (0.5, 0.5)),
    'complete_sets': ('scratch/curated_highres/cat_suites_DSC03045.jpg', (0.5, 0.5)),
    'chains': ('scratch/curated_highres/col_links_layers_DSC03064.jpg', (0.5, 0.5)),
}

for base_name, (src_file, (fx, fy)) in mapping.items():
    with Image.open(src_file) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        side = min(w, h)
        cx, cy = int(w * fx), int(h * fy)
        x0 = max(0, min(w - side, cx - side // 2))
        y0 = max(0, min(h - side, cy - side // 2))
        cropped = rgb.crop((x0, y0, x0 + side, y0 + side))
        resized = cropped.resize((800, 800), Image.Resampling.LANCZOS)
        enh = ImageEnhance.Sharpness(resized).enhance(1.15)
        
        for d in targets:
            enh.save(os.path.join(d, f"{base_name}.webp"), format='WEBP', quality=90)
            enh.save(os.path.join(d, f"{base_name}.jpg"), format='JPEG', quality=90)
            enh.save(os.path.join(d, f"{base_name}.png"), format='PNG')
        print(f"Saved {base_name}.webp/.jpg/.png")

print("All category formats overwritten with authentic drive assets!")


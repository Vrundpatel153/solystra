import os
from PIL import Image, ImageEnhance

targets_cat = [
    'jewellery-design-html/solystra_assets/categories/zavya_style',
    'jewellery-design-html-dist/solystra_assets/categories/zavya_style',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\categories\zavya_style',
    'public/solystra_assets/categories/zavya_style'
]

targets_col = [
    'jewellery-design-html/solystra_assets/collections',
    'jewellery-design-html-dist/solystra_assets/collections',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\collections',
    'public/solystra_assets/collections'
]

extra_cat = {
    'chains.webp': ('scratch/curated_highres/col_links_layers_DSC03064.jpg', (0.5, 0.5)),
    'complete_sets.webp': ('scratch/curated_highres/cat_suites_DSC03045.jpg', (0.5, 0.5)),
}

extra_col = {
    'collection_drops.webp': ('scratch/curated_highres/col_drops_halo_DSC03109.jpg', (0.5, 0.5)),
    'collection_ombre.webp': ('scratch/curated_highres/col_daily_luxe_DSC03116.jpg', (0.5, 0.5)),
}

def process_dict(mapping, target_dirs, out_size=(600, 600)):
    for out_name, (src_file, (fx, fy)) in mapping.items():
        with Image.open(src_file) as im:
            rgb = im.convert('RGB')
            w, h = rgb.size
            side = min(w, h)
            cx, cy = int(w * fx), int(h * fy)
            x0 = max(0, min(w - side, cx - side // 2))
            y0 = max(0, min(h - side, cy - side // 2))
            cropped = rgb.crop((x0, y0, x0 + side, y0 + side))
            resized = cropped.resize(out_size, Image.Resampling.LANCZOS)
            enh = ImageEnhance.Sharpness(resized).enhance(1.12)
            for d in target_dirs:
                enh.save(os.path.join(d, out_name), format='WEBP', quality=90, method=6)
            print(f"Saved {out_name}")

process_dict(extra_cat, targets_cat)
process_dict(extra_col, targets_col)
print("Extra assets successfully processed!")

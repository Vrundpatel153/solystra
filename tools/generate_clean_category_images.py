import os
import gc
from PIL import Image

# Output directories to update
dest_dirs = [
    'jewellery-design-html/solystra_assets/categories/zavya_style',
    'jewellery-design-html-dist/solystra_assets/categories/zavya_style',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\categories\zavya_style',
    'public/solystra_assets/categories/zavya_style',
]

collections_dirs = [
    'jewellery-design-html/solystra_assets/collections',
    'jewellery-design-html-dist/solystra_assets/collections',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\collections',
    'public/solystra_assets/collections',
]

for d in dest_dirs + collections_dirs:
    os.makedirs(d, exist_ok=True)

# Image tasks definition
tasks = [
    {
        'filename': 'necklaces.webp',
        'src': 'scratch/drive_photos/DSC02659.JPG',
        'crop': (0, 150, 800, 950),
        'dirs': dest_dirs
    },
    {
        'filename': 'complete_sets.webp',
        'src': 'scratch/drive_photos/DSC02669.JPG',
        'crop': (155, 75, 505, 425),
        'dirs': dest_dirs
    },
    {
        'filename': 'mangalsutras.webp',
        'src': 'scratch/drive_photos/DSC02667.JPG',
        'crop': (0, 0, 480, 480),
        'dirs': dest_dirs
    },
    {
        'filename': 'chains.webp',
        'src': 'scratch/drive_photos/DSC02660.JPG',
        'crop': (150, 0, 683, 533),
        'dirs': dest_dirs
    },
    {
        'filename': 'collection_drops.webp',
        'src': 'scratch/drive_photos/DSC02673.JPG',
        'crop': (155, 85, 505, 435),
        'dirs': collections_dirs
    },
    {
        'filename': 'collection_drops.jpg',
        'src': 'scratch/drive_photos/DSC02673.JPG',
        'crop': (155, 85, 505, 435),
        'dirs': collections_dirs
    },
    {
        'filename': 'collection_ombre.webp',
        'src': 'scratch/drive_photos/DSC02674.JPG',
        'crop': (150, 0, 683, 533),
        'dirs': collections_dirs
    },
    {
        'filename': 'collection_ombre.jpg',
        'src': 'scratch/drive_photos/DSC02674.JPG',
        'crop': (150, 0, 683, 533),
        'dirs': collections_dirs
    },
    {
        'filename': 'collection_studs.webp',
        'src': 'scratch/drive_photos/DSC02673.JPG',
        'crop': (155, 85, 505, 435),
        'dirs': collections_dirs
    },
    {
        'filename': 'collection_studs.jpg',
        'src': 'scratch/drive_photos/DSC02673.JPG',
        'crop': (155, 85, 505, 435),
        'dirs': collections_dirs
    },
    {
        'filename': 'bracelets.webp',
        'src': 'jewellery-design-html/solystra_assets/categories/cat_bracelets.webp',
        'crop': None,
        'dirs': dest_dirs
    },
    {
        'filename': 'rings.webp',
        'src': 'jewellery-design-html/solystra_assets/categories/cat_rings.webp',
        'crop': None,
        'dirs': dest_dirs
    },
    {
        'filename': 'earrings.webp',
        'src': 'jewellery-design-html/solystra_assets/categories/cat_earrings.webp',
        'crop': None,
        'dirs': dest_dirs
    },
    {
        'filename': 'anklets.webp',
        'src': 'jewellery-design-html/solystra_assets/categories/cat_anklets.webp',
        'crop': None,
        'dirs': dest_dirs
    },
]

print(f"Starting processing of {len(tasks)} images...")

for t in tasks:
    fname = t['filename']
    src = t['src']
    crop = t['crop']
    targets = t['dirs']
    
    if not os.path.exists(src):
        print(f"Warning: source not found: {src}")
        continue

    try:
        with Image.open(src) as img:
            img = img.convert('RGB')
            if crop:
                c = img.crop(crop)
            else:
                # Square center crop if not already square
                w, h = img.size
                if w != h:
                    side = min(w, h)
                    x0 = (w - side) // 2
                    y0 = (h - side) // 2
                    c = img.crop((x0, y0, x0 + side, y0 + side))
                else:
                    c = img.copy()
            
            c = c.resize((800, 800), Image.Resampling.LANCZOS)
            
            is_webp = fname.endswith('.webp')
            ext_format = 'WEBP' if is_webp else 'JPEG'
            save_kwargs = {'quality': 88, 'method': 6} if is_webp else {'quality': 88}
            
            for d in targets:
                if os.path.exists(d):
                    out_path = os.path.join(d, fname)
                    c.save(out_path, format=ext_format, **save_kwargs)
            
            del c
        del img
    except Exception as e:
        print(f"Error processing {fname}: {e}")
    
    gc.collect()
    print(f"Generated {fname} successfully.")

print("All category and collection images generated!")


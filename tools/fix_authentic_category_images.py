import os
from PIL import Image, ImageEnhance

dest_dirs = [
    'jewellery-design-html/solystra_assets/categories/zavya_style',
    'jewellery-design-html-dist/solystra_assets/categories/zavya_style',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\categories\zavya_style',
    'public/solystra_assets/categories/zavya_style',
    'jewellery-design-html/solystra_assets/categories',
    'jewellery-design-html-dist/solystra_assets/categories',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\categories',
    'public/solystra_assets/categories',
]

for d in dest_dirs:
    os.makedirs(d, exist_ok=True)

# Map category to authentic, high-definition, verified studio product shot
cat_sources = {
    # 1. Bracelets & Kadas: Pure 925 silver pave link slider bracelet / tennis bracelet
    'bracelets': 'jewellery-design-html/solystra_assets/products/pave-link-slider-bracelet-925-sterling-silver/angle_1.webp',
    # 2. Rings & Bands: Sparkling oval halo solitaire band ring
    'rings': 'jewellery-design-html/solystra_assets/products/oval-halo-band-ring/angle_1.webp',
    # 3. Earrings & Studs: Elegant 18K / pure 925 arc bar hoops / studs
    'earrings': 'jewellery-design-html/solystra_assets/products/arc-bar-hoops/angle_1.webp',
    # 4. Necklaces & Pendants: Atelier signature solitaire accent circle necklace
    'necklaces': 'jewellery-design-html/solystra_assets/products/accent-circle-925-silver-necklace/angle_1.webp',
    # 5. Gift Suites & Sets: Amethyst bloom floral necklace & earrings heirloom suite
    'complete_sets': 'jewellery-design-html/solystra_assets/products/amethyst-bloom-necklace-set-925-sterling-silver/angle_1.webp',
    # 6. Anklets & Payals: Floral crystal silver charm anklet
    'anklets': 'jewellery-design-html/solystra_assets/products/floral-crystal-anklet-set-925-sterling-silver/angle_1.webp',
    # 7. Layering Chains: Fine box / dainty link chain
    'chains': 'jewellery-design-html/solystra_assets/products/fine-box-rose-gold-chain/angle_1.webp',
    # 8. Sacred Mangalsutras
    'mangalsutras': 'jewellery-design-html/solystra_assets/products/accent-circle-925-silver-necklace/angle_1.webp',
    # 9. Solitaire Nose Pins / Studs
    'nose_pins': 'jewellery-design-html/solystra_assets/products/round-stud/angle_1.webp',
    # 10. Men's Silver Collection
    'mens': 'jewellery-design-html/solystra_assets/products/classic-ridge-band/angle_1.webp',
}

print("Updating authentic Category images across all target folders...")

for cat_name, src in cat_sources.items():
    if not os.path.exists(src):
        print(f"Warning: Source not found for {cat_name}: {src}")
        continue
    
    with Image.open(src) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        # Center square crop
        side = min(w, h)
        x0 = (w - side) // 2
        y0 = (h - side) // 2
        square_crop = rgb.crop((x0, y0, x0 + side, y0 + side))
        square_crop = square_crop.resize((800, 800), Image.Resampling.LANCZOS)
        square_crop = ImageEnhance.Sharpness(square_crop).enhance(1.08)
        
        for d in dest_dirs:
            square_crop.save(os.path.join(d, f"{cat_name}.webp"), format='WEBP', quality=92, method=6)
            square_crop.save(os.path.join(d, f"{cat_name}.jpg"), format='JPEG', quality=92)
            # Also for legacy filenames
            if cat_name in ['bracelets', 'rings', 'earrings', 'anklets', 'necklaces']:
                square_crop.save(os.path.join(d, f"cat_{cat_name}.webp"), format='WEBP', quality=92, method=6)
                square_crop.save(os.path.join(d, f"cat_{cat_name}.jpg"), format='JPEG', quality=92)
                
        print(f"✓ Fixed {cat_name} category image from '{src}'")

print("All category images updated with authentic Solystra products!")


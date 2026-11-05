import os
import shutil
from PIL import Image

src_v1 = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\solystra_luxury_banner_bronze_fullbleed_1793840547183.jpg'
src_v2 = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\solystra_luxury_banner_champagne_bronze_1793840568053.jpg'

im_v1 = Image.open(src_v1)
im_v2 = Image.open(src_v2)

target_dirs = [
    'jewellery-design-html/solystra_assets/promos',
    'jewellery-design-html-dist/solystra_assets/promos',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\promos',
    'solystra_assets/promos',
    'public/solystra_assets/promos',
    'dist/solystra_assets/promos'
]

for d in target_dirs:
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)
    
    # Save primary banner (V1 - Deep Bronze Velvet)
    webp_path = os.path.join(d, 'atelier_luxury_banner.webp')
    jpg_path = os.path.join(d, 'atelier_luxury_banner.jpg')
    im_v1.save(webp_path, 'WEBP', quality=92)
    im_v1.save(jpg_path, 'JPEG', quality=92)
    print(f"Updated primary banner in {d}")
    
    # Also save V2 (Champagne Bronze) as alternative
    champ_webp = os.path.join(d, 'atelier_luxury_banner_champagne.webp')
    champ_jpg = os.path.join(d, 'atelier_luxury_banner_champagne.jpg')
    im_v2.save(champ_webp, 'WEBP', quality=92)
    im_v2.save(champ_jpg, 'JPEG', quality=92)

print("All banners deployed successfully!")


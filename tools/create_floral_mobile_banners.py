import os
from PIL import Image

BANNERS_DIR = os.path.abspath('jewellery-design-html/solystra_assets/banners')

def make_mobile_crop(src_png, dest_webp, target_width=1024, target_height=1536):
    im = Image.open(src_png)
    w, h = im.size
    
    # Target aspect ratio is 1024 / 1536 = 2 / 3
    target_ratio = target_width / target_height # 0.6667
    src_ratio = w / h # e.g. 1774 / 887 = 2.0
    
    # We want a portrait crop centered on the jewelry model
    # Height is full, width is h * target_ratio
    crop_w = int(h * target_ratio)
    crop_h = h
    # Center horizontally
    left = (w - crop_w) // 2
    right = left + crop_w
    top = 0
    bottom = h
    
    cropped = im.crop((left, top, right, bottom))
    resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
    if resized.mode in ('RGBA', 'LA'):
        resized = resized.convert('RGBA')
    else:
        resized = resized.convert('RGB')
    resized.save(dest_webp, 'WEBP', quality=92, method=6)
    print(f"Created mobile banner: {os.path.basename(dest_webp)} ({target_width}x{target_height}) - {os.path.getsize(dest_webp)//1024} KB")

# 1. Floral Portrait
make_mobile_crop(
    'scratch/drive_raw_downloads/Serene Floral Jewelry Portrait.png',
    os.path.join(BANNERS_DIR, 'banner_floral_portrait_mob.webp')
)

# 2. Profile Floral
make_mobile_crop(
    'scratch/drive_raw_downloads/Serene Profile with Floral Jewelry.png',
    os.path.join(BANNERS_DIR, 'banner_profile_floral_mob.webp')
)


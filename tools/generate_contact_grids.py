import os
from PIL import Image, ImageDraw, ImageFont

thumb_dir = 'scratch/drive_thumbnails'
out_dir = 'scratch/grids'
os.makedirs(out_dir, exist_ok=True)

groups = [
    ('yellow_dress_2719_2758', range(2719, 2759)),
    ('yellow_dress_2759_2799', range(2759, 2800)),
    ('black_blazer_2800_2839', range(2800, 2840)),
    ('black_blazer_2840_2879', range(2840, 2880)),
    ('black_blazer_2880_2899', range(2880, 2900)),
    ('green_dress_2900_2939', range(2900, 2940)),
    ('green_dress_2940_2979', range(2940, 2980)),
    ('green_dress_2980_2999', range(2980, 3000)),
    ('still_life_3000_3039', range(3000, 3040)),
    ('still_life_3040_3079', range(3040, 3080)),
    ('still_life_3080_3099', range(3080, 3100)),
    ('lookbook_3100_3117', range(3100, 3118)),
]

tile_w, tile_h = 140, 180
cols = 8

for name, seq_range in groups:
    files = [f"DSC0{i}.JPG" for i in seq_range if os.path.exists(os.path.join(thumb_dir, f"DSC0{i}.JPG"))]
    if not files:
        continue
    
    rows = (len(files) + cols - 1) // cols
    grid_w = cols * tile_w
    grid_h = rows * (tile_h + 24)
    
    grid = Image.new('RGB', (grid_w, grid_h), color=(20, 20, 20))
    draw = ImageDraw.Draw(grid)
    
    for idx, fname in enumerate(files):
        c = idx % cols
        r = idx // cols
        x = c * tile_w
        y = r * (tile_h + 24)
        
        p = os.path.join(thumb_dir, fname)
        try:
            with Image.open(p) as im:
                im_thumb = im.copy()
                im_thumb.thumbnail((tile_w, tile_h), Image.Resampling.LANCZOS)
                # paste centered in tile
                px = x + (tile_w - im_thumb.width) // 2
                py = y + (tile_h - im_thumb.height) // 2
                grid.paste(im_thumb, (px, py))
                del im_thumb
        except Exception as e:
            pass
        
        draw.text((x + 6, y + tile_h + 4), fname.replace('.JPG', ''), fill=(200, 200, 200))
    
    out_path = os.path.join(out_dir, f"{name}.jpg")
    grid.save(out_path, quality=85)
    print(f"Saved {out_path} ({len(files)} photos)")
    del grid

print("All contact sheets generated.")

from PIL import Image, ImageDraw

def make_numbered_grid(img_path, out_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    draw = ImageDraw.Draw(im)
    
    # Draw vertical lines every 100px
    for x in range(0, w, 100):
        draw.line([(x, 0), (x, h)], fill=(255, 0, 0), width=1)
        draw.text((x + 2, 5), f"{x}", fill=(255, 255, 0))
        draw.text((x + 2, 500), f"{x}", fill=(255, 255, 0))
        draw.text((x + 2, 1000), f"{x}", fill=(255, 255, 0))
        
    # Draw horizontal lines every 100px
    for y in range(0, h, 100):
        draw.line([(0, y), (w, y)], fill=(255, 0, 0), width=1)
        draw.text((5, y + 2), f"{y}", fill=(255, 255, 0))
        draw.text((500, y + 2), f"{y}", fill=(255, 255, 0))
        
    im.save(out_path, quality=90)
    print(f"Saved {out_path}")

make_numbered_grid('scratch/curated_raw/second_combo.png', 'scratch/c2_numbered_grid.jpg')
make_numbered_grid('scratch/curated_raw/golden_meadow_set_combo.png', 'scratch/gm_numbered_grid.jpg')


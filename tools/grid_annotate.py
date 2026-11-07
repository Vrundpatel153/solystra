from PIL import Image, ImageDraw, ImageFont
import os

img1_path = "jewellery-design-html/solystra_assets/curated/curated_look_combo2.webp"
img2_path = "jewellery-design-html/solystra_assets/curated/curated_look_golden_meadow.webp"

out_dir = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"
os.makedirs(out_dir, exist_ok=True)

def annotate_grid(img_path, out_name):
    im = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(im)
    w, h = im.size
    
    # Draw grid every 10%
    for x_pct in range(0, 101, 10):
        x = int(w * x_pct / 100)
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 128), width=1)
        draw.text((x + 2, 10), f"{x_pct}%", fill=(255, 215, 0))
        
    for y_pct in range(0, 101, 10):
        y = int(h * y_pct / 100)
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 128), width=1)
        draw.text((10, y + 2), f"{y_pct}%", fill=(255, 215, 0))
        
    out_path = os.path.join(out_dir, out_name)
    im.save(out_path, quality=85)
    print(f"Saved {out_path}")

annotate_grid(img1_path, "grid_combo2.jpg")
annotate_grid(img2_path, "grid_golden_meadow.jpg")


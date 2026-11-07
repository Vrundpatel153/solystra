from PIL import Image

def find_exact_coords(grid_img, name):
    im = Image.open(grid_img)
    w, h = im.size
    print(f"=== {name} ===")
    
    # In combo2:
    # Let's crop x: 40% to 70%, y: 40% to 90%
    region = im.crop((int(w * 0.35), int(h * 0.40), int(w * 0.75), int(h * 0.90)))
    region.save(f"scratch/{name}_marked_region.jpg")
    print(f"Saved scratch/{name}_marked_region.jpg")

find_exact_coords("C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/grid_combo2.jpg", "combo2")
find_exact_coords("C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/audit_visuals/grid_golden_meadow.jpg", "meadow")


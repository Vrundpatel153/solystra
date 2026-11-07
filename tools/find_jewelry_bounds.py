from PIL import Image

def find_jewelry_bounds(img_path, name):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    print(f"\n=== Original {name} (1024 x 1536) ===")
    
    # Save slices from y=200 to 1500 every 100px so we can see the full body/face anatomy
    # Specifically:
    # Top of hair, eyes, nose, mouth, earrings, neck, necklace pendant, chest, dress
    for y in range(200, 1400, 150):
        slice_crop = im.crop((0, y, w, min(h, y + 150)))
        slice_crop.save(f"scratch/{name}_slice_y{y}.jpg")
    print(f"Saved slices for {name}")

find_jewelry_bounds('scratch/curated_raw/second_combo.png', 'c2')
find_jewelry_bounds('scratch/curated_raw/golden_meadow_set_combo.png', 'gm')


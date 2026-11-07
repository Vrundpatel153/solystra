from PIL import Image

def describe_image(img_path, prefix):
    im = Image.open(img_path)
    w, h = im.size
    print(f"=== {prefix} (size {w}x{h}) ===")
    
    # Let's save 5x5 sub-crops so we can pinpoint exact coordinates
    for y_step in range(20, 80, 15):
        for x_step in range(20, 80, 20):
            box = (int(w * x_step / 100), int(h * y_step / 100), 
                   int(w * (x_step + 15) / 100), int(h * (y_step + 15) / 100))
            crop = im.crop(box)
            crop.save(f"scratch/{prefix}_x{x_step}_y{y_step}.jpg")
    print(f"Saved sub-crops for {prefix}")

describe_image("jewellery-design-html/solystra_assets/curated/curated_look_combo2.webp", "combo2")
describe_image("jewellery-design-html/solystra_assets/curated/curated_look_golden_meadow.webp", "meadow")


from PIL import Image

for name, filename in [("C2 Earring", "pin_ear_c2_zoom.jpg"), 
                       ("C2 Necklace", "pin_neck_c2_zoom.jpg"), 
                       ("GM Choker", "pin_chok_gm_zoom.jpg")]:
    im = Image.open(f"scratch/{filename}").convert('RGB')
    w, h = im.size
    print(f"\n=== {name} Zoom (Center 40,40) ===")
    center_color = im.getpixel((40, 40))
    print(f"Center pixel: {center_color}")


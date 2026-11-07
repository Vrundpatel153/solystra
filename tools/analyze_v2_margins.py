from PIL import Image

def analyze_v2(filename, name):
    im = Image.open(f"scratch/{filename}").convert('RGB')
    w, h = im.size
    print(f"\n=== {name} ({w}x{h}) ===")
    
    # Check bottom margin: where does the necklace end, and how many pixels of clear space exist below it?
    # Let's inspect rows from bottom up: y = h-1 to 0
    necklace_bottom_y = None
    for y in range(h - 1, int(h * 0.5), -2):
        # check middle column x from 30% to 70%
        row_has_gold_or_pendant = False
        for x in range(int(w * 0.35), int(w * 0.65), 2):
            r, g, b = im.getpixel((x, y))
            if (r > 180 and g > 140 and r - b > 40) or (r > 220 and g > 210 and b > 200):
                row_has_gold_or_pendant = True
                break
        if row_has_gold_or_pendant:
            necklace_bottom_y = y
            break
            
    if necklace_bottom_y is not None:
        margin_bottom = h - necklace_bottom_y
        print(f"Necklace bottom detected at y={necklace_bottom_y}px ({necklace_bottom_y/h*100:.1f}%)")
        print(f"Clearance below necklace to card bottom border: {margin_bottom}px ({margin_bottom/h*100:.1f}%)")
    else:
        print("Could not detect necklace bottom")

analyze_v2("v2_crop_c2_pc.jpg", "C2 Desktop (594x492)")
analyze_v2("v2_crop_c2_mob.jpg", "C2 Mobile (360x422)")
analyze_v2("v2_crop_gm_pc.jpg", "GM Desktop (594x492)")
analyze_v2("v2_crop_gm_mob.jpg", "GM Mobile (360x422)")


from PIL import Image

def analyze_box(filename, name):
    im = Image.open(f"scratch/{filename}").convert('RGB')
    w, h = im.size
    print(f"\n=== {name} ({w}x{h}) ===")
    
    # Let's inspect where the face and ear are:
    # Model's earring: in second combo, she's facing left, ear is on the right side of her head.
    # Model's necklace: on her chest/neck.
    
    # Let's search for brightest gold / skin pixels in ear region (x: 45%-65%, y: 35%-60%)
    ear_pixels = []
    for y in range(int(h * 0.35), int(h * 0.60)):
        for x in range(int(w * 0.45), int(w * 0.65)):
            r, g, b = im.getpixel((x, y))
            # Gold earring has warm high yellow (r > 180, g > 150, b < 130)
            if r > 180 and g > 140 and (r - b) > 50:
                ear_pixels.append((x / w * 100, y / h * 100))
                
    if ear_pixels:
        avg_x = sum(p[0] for p in ear_pixels) / len(ear_pixels)
        avg_y = sum(p[1] for p in ear_pixels) / len(ear_pixels)
        print(f"Earring gold detected: {len(ear_pixels)} px, center at x={avg_x:.1f}%, y={avg_y:.1f}%")
    else:
        print("No specific gold ear pixels found with strict filter")

    # Let's search neck region (x: 40%-70%, y: 60%-90%)
    neck_pixels = []
    for y in range(int(h * 0.60), int(h * 0.90)):
        for x in range(int(w * 0.40), int(w * 0.70)):
            r, g, b = im.getpixel((x, y))
            if (r > 190 and g > 150 and b < 140) or (r > 220 and g > 210 and b > 200):
                neck_pixels.append((x / w * 100, y / h * 100))
    if neck_pixels:
        avg_x = sum(p[0] for p in neck_pixels) / len(neck_pixels)
        avg_y = sum(p[1] for p in neck_pixels) / len(neck_pixels)
        print(f"Necklace/pendant detected: {len(neck_pixels)} px, center at x={avg_x:.1f}%, y={avg_y:.1f}%")

analyze_box("calib_c2_mob.jpg", "C2 Mobile")
analyze_box("calib_c2_pc.jpg", "C2 Desktop")
analyze_box("calib_gm_mob.jpg", "GM Mobile")
analyze_box("calib_gm_pc.jpg", "GM Desktop")

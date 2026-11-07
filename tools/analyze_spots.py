from PIL import Image

def find_bright_spots(img_path, region_name):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    print(f"Analyzing {region_name} ({w}x{h})...")
    # find brightest pixels or high-contrast pixels
    pixels = im.load()
    high_spots = []
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            r, g, b = pixels[x, y]
            # Jewelry in warm/gold: high r, high g, or sparkling white
            brightness = (r + g + b) / 3
            if brightness > 210:
                high_spots.append((x, y, brightness))
    print(f"Total bright spots in {region_name}: {len(high_spots)}")
    if high_spots:
        avg_x = sum(s[0] for s in high_spots) / len(high_spots)
        avg_y = sum(s[1] for s in high_spots) / len(high_spots)
        print(f"Center of bright cluster in {region_name}: x={avg_x:.1f}, y={avg_y:.1f}")

find_bright_spots('scratch/c2_earring_test.jpg', 'c2_earring')
find_bright_spots('scratch/c2_neck_test.jpg', 'c2_neck')
find_bright_spots('scratch/gm_ear_test.jpg', 'gm_ear')
find_bright_spots('scratch/gm_choker_test.jpg', 'gm_choker')

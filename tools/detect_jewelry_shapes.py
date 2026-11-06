import os
from PIL import Image
import numpy as np

thumb_dir = 'scratch/drive_thumbnails'

print("Analyzing jewelry shapes in DSC03000 - DSC03117...")

for i in range(3000, 3118, 5):
    fname = f"DSC0{i}.JPG"
    p = os.path.join(thumb_dir, fname)
    if not os.path.exists(p):
        continue
    
    with Image.open(p) as im:
        arr = np.array(im.convert('RGB'))
        # Brightness
        gray = np.mean(arr, axis=2)
        bright_mask = gray > 100
        total_bright = np.sum(bright_mask)
        
        if total_bright > 50:
            ys, xs = np.where(bright_mask)
            min_y, max_y = np.min(ys), np.max(ys)
            min_x, max_x = np.min(xs), np.max(xs)
            bw = max_x - min_x
            bh = max_y - min_y
            aspect = bw / float(bh) if bh > 0 else 1.0
            print(f"{fname}: bright_pixels={total_bright}, bbox=({bw}x{bh}), aspect={aspect:.2f}, center=({(min_x+max_x)//2}, {(min_y+max_y)//2})")


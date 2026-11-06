import os
from PIL import Image
import numpy as np

thumb_dir = 'scratch/drive_thumbnails'

print("Inspecting still-life / macro series DSC03000 - DSC03117...")

# Let's check color histograms and prominent features
results = []
for i in range(3000, 3118):
    fname = f"DSC0{i}.JPG"
    p = os.path.join(thumb_dir, fname)
    if not os.path.exists(p):
        continue
    
    with Image.open(p) as im:
        arr = np.array(im.convert('RGB'))
        h, w, _ = arr.shape
        
        # Check background colors (corners)
        tl = arr[:30, :30].mean(axis=(0,1))
        br = arr[-30:, -30:].mean(axis=(0,1))
        center = arr[h//3:2*h//3, w//3:2*w//3].mean(axis=(0,1))
        
        # Check if green velvet (low R, high G, low B)
        is_green = center[1] > center[0] * 1.15 and center[1] > center[2] * 1.15
        # Check if dark/black
        is_dark = np.mean(center) < 70
        # Check if bright/white/champagne
        is_bright = np.mean(center) > 160
        
        results.append({
            'fname': fname,
            'is_green': is_green,
            'is_dark': is_dark,
            'is_bright': is_bright,
            'center_rgb': [int(c) for c in center],
            'tl_rgb': [int(c) for c in tl]
        })

print(f"Total analyzed: {len(results)}")
green_count = sum(1 for r in results if r['is_green'])
dark_count = sum(1 for r in results if r['is_dark'])
bright_count = sum(1 for r in results if r['is_bright'])
print(f"Green velvet: {green_count}, Dark/Moody: {dark_count}, Bright/Champagne: {bright_count}")

# Print 10 samples
for r in results[:20]:
    print(r['fname'], 'Center RGB:', r['center_rgb'], 'Green:', r['is_green'], 'Dark:', r['is_dark'])

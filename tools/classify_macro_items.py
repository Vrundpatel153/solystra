import os
from PIL import Image
import numpy as np

thumb_dir = 'scratch/drive_thumbnails'

print("Analyzing all 118 still life files...")
classifications = []

for i in range(3000, 3118):
    fname = f"DSC0{i}.JPG"
    p = os.path.join(thumb_dir, fname)
    if not os.path.exists(p):
        continue
    
    with Image.open(p) as im:
        arr = np.array(im.convert('RGB'))
        gray = np.mean(arr, axis=2)
        
        # Detect bright metal / gems
        bright = gray > 90
        pixel_count = np.sum(bright)
        
        ys, xs = np.where(bright)
        if len(ys) > 20:
            bw = np.max(xs) - np.min(xs)
            bh = np.max(ys) - np.min(ys)
            aspect = bw / float(bh) if bh > 0 else 1.0
            cx, cy = int((np.min(xs) + np.max(xs)) / 2), int((np.min(ys) + np.max(ys)) / 2)
        else:
            bw, bh, aspect, cx, cy = 0, 0, 0, 0, 0
            
        classifications.append({
            'fname': fname,
            'pixels': int(pixel_count),
            'w': bw,
            'h': bh,
            'aspect': round(aspect, 2),
            'cx': cx,
            'cy': cy
        })

# Sort by aspect ratio or size
print("Top 10 wide/horizontal items (potential bracelets/chains/flat-lays):")
for c in sorted(classifications, key=lambda x: -x['aspect'])[:10]:
    print(c)

print("\nTop 10 vertical items (potential drop earrings/pendants/hanging necklaces):")
for c in sorted([c for c in classifications if c['aspect'] > 0], key=lambda x: x['aspect'])[:10]:
    print(c)

print("\nTop 10 compact/square items (potential rings/studs):")
for c in sorted([c for c in classifications if 0.7 <= c['aspect'] <= 1.3 and 100 < c['pixels'] < 5000], key=lambda x: abs(x['aspect'] - 1.0))[:10]:
    print(c)

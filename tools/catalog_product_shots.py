import os
from PIL import Image
import numpy as np

thumb_dir = 'scratch/drive_thumbnails'

# Let's inspect images in 3000-3117
results = []
for i in range(3000, 3118):
    fname = f"DSC0{i}.JPG"
    p = os.path.join(thumb_dir, fname)
    if not os.path.exists(p):
        continue
    im = Image.open(p)
    w, h = im.size
    arr = np.array(im.convert('RGB'))
    
    # Compute center crop brightness vs edge brightness
    ch, cw = h // 4, w // 4
    center_patch = arr[ch:3*ch, cw:3*cw]
    center_bright = np.mean(center_patch)
    edge_bright = (np.mean(arr[:ch, :]) + np.mean(arr[-ch:, :])) / 2.0
    
    results.append({
        'fname': fname,
        'size': (w, h),
        'center_bright': round(float(center_bright), 1),
        'edge_bright': round(float(edge_bright), 1)
    })

print(f"Analyzed {len(results)} still life shots.")
for r in results[:15]:
    print(r)


import os
from PIL import Image
import numpy as np

thumb_dir = 'scratch/drive_thumbnails'

print("Analyzing series for complete model portraits...")

# Let's inspect the files in model_candidates first
for f in sorted(os.listdir('scratch/model_candidates')):
    p = os.path.join('scratch/model_candidates', f)
    with Image.open(p) as im:
        arr = np.array(im.convert('RGB'))
        h, w, _ = arr.shape
        # Top 20% (hair/forehead), middle (eyes/face), lower middle (neck/necklace)
        top_bright = np.mean(arr[:int(h*0.2), :])
        mid_bright = np.mean(arr[int(h*0.2):int(h*0.6), :])
        bot_bright = np.mean(arr[int(h*0.6):, :])
        print(f"Candidate {f}: size=({w}x{h}), top={top_bright:.1f}, mid={mid_bright:.1f}, bot={bot_bright:.1f}")


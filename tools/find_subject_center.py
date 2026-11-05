from PIL import Image
import numpy as np

for fname in ['DSC02659.JPG', 'DSC02667.JPG', 'DSC02668.JPG', 'DSC02673.JPG', 'DSC02674.JPG', 'DSC02660.JPG']:
    path = f'scratch/drive_photos/{fname}'
    img = Image.open(path).convert('L')
    arr = np.array(img)
    # find rows and cols where brightness > 60 (above black velvet)
    bright = np.where(arr > 60)
    if len(bright[0]) > 0:
        min_y, max_y = np.min(bright[0]), np.max(bright[0])
        min_x, max_x = np.min(bright[1]), np.max(bright[1])
        center_y = int(np.mean(bright[0]))
        center_x = int(np.mean(bright[1]))
        print(f"{fname}: img={img.size}, subject bounding y=[{min_y}, {max_y}], x=[{min_x}, {max_x}], center=({center_x}, {center_y})")


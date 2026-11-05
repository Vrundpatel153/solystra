import os
from PIL import Image

os.makedirs('scratch/test_crops', exist_ok=True)

# For each image, let's create a square crop
# DSC02659: (800, 1200), center_y=162 but bounding goes to 1014. Let's try y=0..800 and y=150..950
with Image.open('scratch/drive_photos/DSC02659.JPG') as img:
    crop1 = img.crop((0, 0, 800, 800))
    crop1.save('scratch/test_crops/DSC02659_top.jpg', quality=90)
    crop2 = img.crop((0, 150, 800, 950))
    crop2.save('scratch/test_crops/DSC02659_mid.jpg', quality=90)

# For landscape photos (800x533), square crop with side 533:
landscape_crops = {
    'DSC02667_krishna.jpg': ('scratch/drive_photos/DSC02667.JPG', 267), # x=267..800
    'DSC02668_heart.jpg': ('scratch/drive_photos/DSC02668.JPG', 267),
    'DSC02673_crown.jpg': ('scratch/drive_photos/DSC02673.JPG', 267),
    'DSC02674_rainbow.jpg': ('scratch/drive_photos/DSC02674.JPG', 267),
    'DSC02660_chain.jpg': ('scratch/drive_photos/DSC02660.JPG', 267),
}

for out_name, (src, x_start) in landscape_crops.items():
    with Image.open(src) as img:
        h = img.height
        c = img.crop((x_start, 0, x_start + h, h))
        c = c.resize((800, 800), Image.Resampling.LANCZOS)
        c.save(f'scratch/test_crops/{out_name}', quality=90)

print("Saved test crops successfully!")


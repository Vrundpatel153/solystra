from PIL import Image

crops = {
    'krishna_centered.jpg': ('scratch/drive_photos/DSC02667.JPG', (50, 0, 583, 533)),
    'heart_centered.jpg': ('scratch/drive_photos/DSC02668.JPG', (80, 0, 613, 533)),
    'crown_centered.jpg': ('scratch/drive_photos/DSC02673.JPG', (80, 0, 613, 533)),
    'rainbow_centered.jpg': ('scratch/drive_photos/DSC02674.JPG', (150, 0, 683, 533)),
    'chain_centered.jpg': ('scratch/drive_photos/DSC02660.JPG', (150, 0, 683, 533)),
}

for name, (src, box) in crops.items():
    with Image.open(src) as img:
        c = img.crop(box).resize((800, 800), Image.Resampling.LANCZOS)
        c.save(f'scratch/test_crops/{name}', quality=92)

print("Centered crops generated!")


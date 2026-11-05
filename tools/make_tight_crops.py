from PIL import Image

with Image.open('scratch/drive_photos/DSC02669.JPG') as img:
    c = img.crop((155, 75, 505, 425)).resize((800, 800), Image.Resampling.LANCZOS)
    c.save('scratch/test_crops/heart_tight.jpg', quality=92)

with Image.open('scratch/drive_photos/DSC02673.JPG') as img:
    c = img.crop((155, 85, 505, 435)).resize((800, 800), Image.Resampling.LANCZOS)
    c.save('scratch/test_crops/crown_tight.jpg', quality=92)

print("Tight crops saved!")


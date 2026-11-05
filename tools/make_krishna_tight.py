from PIL import Image

with Image.open('scratch/drive_photos/DSC02667.JPG') as img:
    c = img.crop((45, 35, 395, 385)).resize((800, 800), Image.Resampling.LANCZOS)
    c.save('scratch/test_crops/krishna_tight.jpg', quality=92)

print("Krishna tight crop saved!")


from PIL import Image

with Image.open('scratch/drive_photos/DSC02667.JPG') as img:
    c = img.crop((0, 0, 480, 480)).resize((800, 800), Image.Resampling.LANCZOS)
    c.save('scratch/test_crops/krishna_ideal.jpg', quality=92)

print("Krishna ideal crop saved!")


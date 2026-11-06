import json
import os

with open('scratch/all_drive_jpgs.json', 'r', encoding='utf-8') as f:
    drive_data = json.load(f)

print(f"Total items in all_drive_jpgs.json: {len(drive_data)}")
if isinstance(drive_data, list):
    print("Sample item:", drive_data[0])
elif isinstance(drive_data, dict):
    print("Keys:", list(drive_data.keys())[:10])

# Check how many images are in drive_thumbs or scratch/drive_photos
thumbs = os.listdir('jewellery-design-html/drive_thumbs') if os.path.exists('jewellery-design-html/drive_thumbs') else []
print(f"Thumbnails in jewellery-design-html/drive_thumbs: {len(thumbs)}")

photos = os.listdir('scratch/drive_photos') if os.path.exists('scratch/drive_photos') else []
print(f"Photos in scratch/drive_photos: {len(photos)}")

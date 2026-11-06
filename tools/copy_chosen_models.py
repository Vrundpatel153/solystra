import os
import shutil
from PIL import Image

out_dir = 'scratch/chosen_hero_models'
os.makedirs(out_dir, exist_ok=True)

files = {
    'model_1_solitaire_heart_yellow_dress.jpg': 'scratch/model_check/DSC02715.JPG',
    'model_2_pearl_solitaire_blazer.jpg': 'scratch/model_candidates/DSC02724.JPG',
    'model_3_crown_tiara_blazer.jpg': 'scratch/model_candidates/DSC02745.JPG',
    'model_4_tennis_bracelet_green_dress.jpg': 'scratch/model_candidates/DSC02823.JPG',
}

for dest_name, src_path in files.items():
    dest_path = os.path.join(out_dir, dest_name)
    shutil.copy2(src_path, dest_path)
    with Image.open(dest_path) as img:
        print(f"{dest_name}: {img.size}, {os.path.getsize(dest_path)/1024:.1f} KB")

print("Copied all 4 chosen model images successfully!")


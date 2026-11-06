import shutil
import os

artifact_dir = r'C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98'

refs = {
    'hero_model_ref_1.jpg': 'scratch/chosen_hero_models/model_1_solitaire_heart_yellow_dress.jpg',
    'hero_model_ref_2.jpg': 'scratch/chosen_hero_models/model_2_pearl_solitaire_blazer.jpg',
    'hero_model_ref_3.jpg': 'scratch/chosen_hero_models/model_3_crown_tiara_blazer.jpg',
    'hero_model_ref_4.jpg': 'scratch/chosen_hero_models/model_4_tennis_bracelet_green_dress.jpg',
}

for name, src in refs.items():
    dest = os.path.join(artifact_dir, name)
    shutil.copy2(src, dest)
    print(f"Copied {name} -> {dest} ({os.path.getsize(dest)} bytes)")


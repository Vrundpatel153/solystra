from PIL import Image
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

# Desktop crop of Curated section
im_desk = Image.open(os.path.join(ARTIFACT_DIR, "desktop_combo1_earring_hotspot.jpg"))
# Find curated section crop
crop_desk = im_desk.crop((150, 100, 1290, 750))
crop_desk.save(os.path.join(ARTIFACT_DIR, "crop_desktop_curated_earring.jpg"), quality=92)

# Mobile crop of Curated section
im_mob = Image.open(os.path.join(ARTIFACT_DIR, "mobile_combo2_golden_meadow_hotspot.jpg"))
crop_mob = im_mob.crop((0, 0, 780, 1000))
crop_mob.save(os.path.join(ARTIFACT_DIR, "crop_mobile_curated_golden_meadow.jpg"), quality=92)

print("Crops saved successfully!")

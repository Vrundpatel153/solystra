from PIL import Image
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

# Inspect desktop_collections_view
im_desk = Image.open(os.path.join(ARTIFACT_DIR, "desktop_collections_view.jpg"))
crop_desk = im_desk.crop((0, 0, 1440, 800))
crop_desk.save(os.path.join(ARTIFACT_DIR, "crop_desktop_collections.jpg"), quality=90)

# Inspect mobile_collections_view
im_mob = Image.open(os.path.join(ARTIFACT_DIR, "mobile_collections_view.jpg"))
crop_mob = im_mob.crop((0, 0, 780, 1400))
crop_mob.save(os.path.join(ARTIFACT_DIR, "crop_mobile_collections.jpg"), quality=90)

print("Crops saved!")


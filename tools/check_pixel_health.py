from PIL import Image
import os
import numpy as np

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

for fname in ["desktop_hero_slide2_banner3.jpg", "desktop_hero_slide3_banner4.jpg", "crop_desktop_collections.jpg", "mobile_hero_slide2_banner3.jpg", "mobile_hero_slide3_banner4.jpg", "crop_mobile_collections.jpg"]:
    p = os.path.join(ARTIFACT_DIR, fname)
    im = Image.open(p)
    arr = np.array(im)
    print(f"{fname}: mean={arr.mean():.1f}, std={arr.std():.1f}, min={arr.min()}, max={arr.max()}")


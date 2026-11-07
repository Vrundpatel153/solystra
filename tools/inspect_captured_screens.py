from PIL import Image
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

images = [
    "desktop_hero_slide2_banner3.jpg",
    "desktop_hero_slide3_banner4.jpg",
    "desktop_collections_view.jpg",
    "mobile_hero_slide2_banner3.jpg",
    "mobile_hero_slide3_banner4.jpg",
    "mobile_collections_view.jpg"
]

for img_name in images:
    p = os.path.join(ARTIFACT_DIR, img_name)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{img_name}: size={im.size}, mode={im.mode}")
    else:
        print(f"Missing: {img_name}")


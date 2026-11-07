from PIL import Image
import os

ARTIFACT_DIR = r"C:\Users\vrund\.gemini\antigravity\brain\68f27351-9b2c-41bf-b75f-ce5ad9262a98\audit_visuals"

files = [
    "desktop_combo1_earring_hotspot.jpg",
    "desktop_combo1_necklace_hotspot.jpg",
    "desktop_combo2_golden_meadow_hotspot.jpg",
    "mobile_combo2_golden_meadow_hotspot.jpg"
]

for f in files:
    p = os.path.join(ARTIFACT_DIR, f)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{f}: size={im.size}, mode={im.mode}")

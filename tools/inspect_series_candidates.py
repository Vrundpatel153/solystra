import os
from PIL import Image

thumbs_dir = 'jewellery-design-html/drive_thumbs'
files = sorted([f for f in os.listdir(thumbs_dir) if f.endswith('.JPG')])

print(f"Total downloaded thumbnails in {thumbs_dir}: {len(files)}")

# Let's inspect by series
series = {
    "Yellow Top / Necklaces & Pendants (DSC02719-DSC02799)": [f for f in files if "DSC027" in f],
    "Black Blazer / Tiara, Earrings & Glamour (DSC02800-DSC02898)": [f for f in files if "DSC028" in f],
    "Sage Green Dress / Tennis Bracelets & Rings (DSC02899-DSC02998)": [f for f in files if "DSC029" in f],
    "Emerald Velvet & Macro Still Life (DSC02999-DSC03099)": [f for f in files if "DSC030" in f],
    "Lookbook & Signature Suites (DSC03100-DSC03117)": [f for f in files if "DSC031" in f]
}

for sname, sfiles in series.items():
    print(f"\n=== {sname}: {len(sfiles)} files ===")
    print("  First 5:", sfiles[:5])
    print("  Last 5:", sfiles[-5:])


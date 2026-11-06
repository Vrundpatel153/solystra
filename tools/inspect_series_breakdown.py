import os
from PIL import Image

thumb_dir = 'scratch/drive_thumbnails'

# Inspect range 3000 to 3099
files = [f"DSC0{i}.JPG" for i in range(3000, 3100)]
existing = [f for f in files if os.path.exists(os.path.join(thumb_dir, f))]

print(f"Total existing in 3000-3099: {len(existing)}")

# Also inspect range 2720-2750, 2800-2850, 2900-2950
for prefix, r in [('27xx (Yellow Dress)', range(2720, 2760)),
                 ('28xx (Black Blazer)', range(2800, 2840)),
                 ('29xx (Sage Green)', range(2900, 2940)),
                 ('30xx (Still Life/Macro)', range(3000, 3050)),
                 ('30xx (Still Life/Macro Part 2)', range(3050, 3100)),
                 ('31xx (Final Suites)', range(3100, 3118))]:
    present = [f"DSC0{i}.JPG" for i in r if os.path.exists(os.path.join(thumb_dir, f"DSC0{i}.JPG"))]
    print(f"{prefix}: {len(present)} photos present")

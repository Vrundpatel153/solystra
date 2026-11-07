import os
import shutil

SOURCE_DIR = r"c:\Users\vrund\OneDrive\Desktop\jewellery-design\jewellery-design-html"
TARGET_DIST = r"c:\Users\vrund\OneDrive\Desktop\jewellery-design\jewellery-design-html-dist"
TARGET_SOLYSTRA = r"c:\Users\vrund\OneDrive\Desktop\solystra-html"

def sync_dir(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst, exist_ok=True)
    count = 0
    for root, dirs, files in os.walk(src):
        # Ignore git
        if ".git" in root:
            continue
        rel = os.path.relpath(root, src)
        dest_root = os.path.join(dst, rel)
        os.makedirs(dest_root, exist_ok=True)
        for f in files:
            src_f = os.path.join(root, f)
            dst_f = os.path.join(dest_root, f)
            # check if different
            if not os.path.exists(dst_f) or os.path.getmtime(src_f) > os.path.getmtime(dst_f) or os.path.getsize(src_f) != os.path.getsize(dst_f):
                shutil.copy2(src_f, dst_f)
                count += 1
    print(f"Synced {count} files to {dst}")

sync_dir(SOURCE_DIR, TARGET_DIST)
sync_dir(SOURCE_DIR, TARGET_SOLYSTRA)
print("Synchronization complete!")

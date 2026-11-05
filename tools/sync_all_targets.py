import os
import shutil

src_dir = os.path.abspath('jewellery-design-html')
targets = [
    os.path.abspath('jewellery-design-html-dist'),
    os.path.abspath(r'c:\Users\vrund\OneDrive\Desktop\solystra-html')
]

for dest_dir in targets:
    print(f"Syncing to {dest_dir}...")
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_root = os.path.join(dest_dir, rel_path)
        os.makedirs(target_root, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(target_root, file)
            copy_needed = True
            if os.path.exists(dest_file):
                if os.path.getmtime(src_file) <= os.path.getmtime(dest_file) and os.path.getsize(src_file) == os.path.getsize(dest_file):
                    copy_needed = False
            if copy_needed:
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {os.path.relpath(dest_file, dest_dir)}")

print("All targets synchronized successfully!")


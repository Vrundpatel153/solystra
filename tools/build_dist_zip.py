import os
import zipfile
import time

def build_dist_zip():
    dist_dir = 'jewellery-design-html-dist'
    zip_path = 'jewellery-design-html-dist.zip'
    t0 = time.time()
    print(f"Building {zip_path} from {dist_dir}...")

    # Use a temp file first so we don't corrupt existing
    tmp_zip = zip_path + ".tmp"
    with zipfile.ZipFile(tmp_zip, 'w') as zf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dist_dir)
                ext = os.path.splitext(file)[1].lower()
                # If already compressed binary image, store it without re-compressing
                if ext in ['.webp', '.png', '.jpg', '.jpeg', '.gif', '.woff', '.woff2']:
                    zf.write(full_path, rel_path, compress_type=zipfile.ZIP_STORED)
                else:
                    zf.write(full_path, rel_path, compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)

    if os.path.exists(zip_path):
        os.remove(zip_path)
    os.rename(tmp_zip, zip_path)
    dur = time.time() - t0
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Zip built in {dur:.2f}s! Size: {size_mb:.2f} MB")

if __name__ == '__main__':
    build_dist_zip()

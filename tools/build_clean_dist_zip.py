import os
import zipfile

def make_zip(source_dir, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    dist_dir = os.path.join(root_dir, 'dist')
    zip_path = os.path.join(root_dir, 'dist.zip')
    if os.path.exists(dist_dir):
        make_zip(dist_dir, zip_path)
        print(f"Created {zip_path}")

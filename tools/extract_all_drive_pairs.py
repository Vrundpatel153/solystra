import re

with open('scratch/drive_html_dump.txt', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern: <div class="JxSEve" aria-label="([^"]+)"[^>]*>[\s\S]*?data-id="([^"]+)"
matches = re.findall(r'aria-label="([^"]+)"[^>]*?>[\s\S]*?data-id="([a-zA-Z0-9_-]{25,})"', html)
print(f"Parsed {len(matches)} item-id pairs:")
for label, fid in matches:
    print(f"  {label:<40} -> {fid}")

# Also check for other subfolders
folders = re.findall(r'aria-label="([^"]*folder[^"]*)"[^>]*?>[\s\S]*?data-id="([a-zA-Z0-9_-]{25,})"', html, re.I)
print(f"\nFolders specifically: {len(folders)}")
for flabel, fid in folders:
    print(f"  {flabel:<40} -> {fid}")


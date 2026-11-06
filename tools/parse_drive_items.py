import re
import json

with open('scratch/drive_html_dump.txt', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern for files
# aria-label="DSC02659.ARW Image Shared" data-handled-by-drag-and-drop="true" ssk='5:auSv138:1SKZHsAAl0qD3fk50GHCyG9dl1g9a1wJG-0-16'
# or data-id or ssk
items = re.findall(r'aria-label="([^"]+)"[^>]*?data-id="([^"]+)"', html)
print("Pattern 1 (aria-label + data-id):", len(items))

# Pattern 2: aria-label with DSC or folder or anything
aria_labels = re.findall(r'aria-label="([^"]+)"', html)
print("Total aria-labels:", len(aria_labels))

drive_items = []
for a in aria_labels:
    if any(k in a.lower() for k in ['dsc', 'image', 'shared', 'folder', 'arw', 'jpg', 'jpeg', 'png']):
        drive_items.append(a)

print(f"Drive items found in aria-labels: {len(drive_items)}")
for it in drive_items[:30]:
    print(" ", it)

# Also find Google Drive file IDs
# Typically in data-id="<id>" or ["<id>", ...]
fids = re.findall(r'data-id="([a-zA-Z0-9_-]{25,})"', html)
print(f"Found {len(fids)} unique data-ids: {len(set(fids))}")

# Check ssk or jsdata
ssk_matches = re.findall(r'aria-label="([^"]+)"[^>]*?data-target="item"[^>]*?data-id="([^"]+)"', html)
print("Item matches with data-target=item:", len(ssk_matches))

# Let's inspect the exact HTML snippet around one item
pos = html.find('DSC02659')
print("\nExact snippet around DSC02659:")
print(html[max(0, pos-200):pos+400])

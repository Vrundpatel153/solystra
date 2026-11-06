import json

with open('scratch/all_drive_jpgs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total JPG files cataloged: {len(data)}")
names = sorted(data.keys())
print(f"First: {names[0]}, Last: {names[-1]}")

# Group into ranges
groups = {}
for name in names:
    prefix = name[:6] # e.g. DSC026, DSC027
    groups[prefix] = groups.get(prefix, 0) + 1

print("\nBreakdown by series:")
for k, count in sorted(groups.items()):
    print(f"  {k}xx.JPG: {count} images")

import json

with open('C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/.system_generated/steps/3910/output.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Extract json
start = raw.find('{')
end = raw.rfind('}') + 1
data = json.loads(raw[start:end])

print(f"Total JPGs found: {data['count']}")
print(f"Range: {data['range']}")

with open('scratch/all_drive_jpgs.json', 'w', encoding='utf-8') as f:
    json.dump(data['allJpgs'], f, indent=2)

print("Saved to scratch/all_drive_jpgs.json")


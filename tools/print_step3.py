import json

with open('C:/Users/vrund/.gemini/antigravity/brain/98322512-3215-46cb-b415-bc55050c917f/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    lines = [json.loads(l) for l in f]

step3 = lines[3]
print("Tool calls in Step 3:")
for tc in step3.get('tool_calls', []):
    print(tc['name'])
    for k, v in tc['args'].items():
        print(f"  {k}: {str(v)[:150]}")


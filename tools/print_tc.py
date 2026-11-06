import json

with open('C:/Users/vrund/.gemini/antigravity/brain/98322512-3215-46cb-b415-bc55050c917f/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        print(f"Line {i}: source={data.get('source')} type={data.get('type')}")
        if data.get('tool_calls'):
            for tc in data['tool_calls']:
                print(f"  tool_call: {tc.get('name')}, args: {list(tc.get('args', {}).keys())}")


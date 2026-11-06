import json

with open('C:/Users/vrund/.gemini/antigravity/brain/98322512-3215-46cb-b415-bc55050c917f/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if 'tool_declarations' in data:
            print("Found tool_declarations:")
            for tool in data['tool_declarations']:
                print(tool.get('name'), tool.get('description'))
        elif 'tools' in data:
            print("Found tools:", data['tools'])


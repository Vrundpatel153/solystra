import re

with open('C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/.system_generated/steps/3884/output.txt', 'r', encoding='utf-8') as f:
    c = f.read()

for line in c.split('\n'):
    if any(k in line.lower() for k in ['folder', 'row', 'gridcell', 'button "heart', 'dsc', 'model', 'raw']):
        print(line[:120])


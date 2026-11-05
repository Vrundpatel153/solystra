import re

with open('C:/Users/vrund/.gemini/antigravity/brain/68f27351-9b2c-41bf-b75f-ce5ad9262a98/.system_generated/steps/3768/output.txt', 'r', encoding='utf-8') as f:
    c = f.read()

headings = re.findall(r'heading "(.*?)"', c)
for h in headings[:15]:
    print('Product heading:', h)


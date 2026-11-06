with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# search for mobile menu
idx = content.find('id="mobile-menu"')
if idx != -1:
    print("Mobile menu found:")
    print(content[idx:idx+2500])
else:
    print("No mobile-menu id, searching for mobile drawer...")
    # search for drawer
    import re
    matches = re.findall(r'<div[^>]*id="[^"]*mobile[^"]*"[^>]*>', content)
    print("Mobile containers:", matches)


import os

for ip in [
    'jewellery-design-html/index.html',
    'jewellery-design-html-dist/index.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\index.html'
]:
    if os.path.exists(ip):
        with open(ip, 'r', encoding='utf-8') as f:
            c = f.read()
        new_c = c.replace('css/styles.css?v=atelier2026_v3', 'css/styles.css?v=editorial_hero_v12')
        if new_c != c:
            with open(ip, 'w', encoding='utf-8') as f:
                f.write(new_c)
            print(f"Busted CSS cache in {ip}")

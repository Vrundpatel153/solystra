from bs4 import BeautifulSoup

with open('jewellery-design-html/index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

panel = soup.find(id='collections-dropdown-panel')
if panel:
    print("Found collections-dropdown-panel!")
    # print desktop and mobile parts
    desktop_grid = panel.find('div', class_=lambda c: c and 'lg:grid' in c)
    mob_panel = panel.find('div', class_=lambda c: c and 'lg:hidden' in c)
    
    print("\n--- DESKTOP GRID ---")
    if desktop_grid:
        for i, col in enumerate(desktop_grid.find_all('div', recursive=False)):
            print(f"\n[Col {i+1}] {col.get('class')}")
            # print headers and buttons
            for b in col.find_all('button'):
                print("  btn:", b.get_text(strip=True)[:50], "->", b.get('onclick'))
            for a in col.find_all('a'):
                print("  link:", a.get_text(strip=True)[:50], "->", a.get('href'))
                
    print("\n--- MOBILE PANEL ---")
    if mob_panel:
        for b in mob_panel.find_all('button'):
            print("  btn:", b.get_text(strip=True)[:50], "->", b.get('onclick'))

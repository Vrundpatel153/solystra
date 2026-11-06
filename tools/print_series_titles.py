from bs4 import BeautifulSoup

with open('jewellery-design-html/drive_audit_contact_sheet.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

for st in soup.find_all('div', class_='series-title'):
    print(st.get_text(strip=True))


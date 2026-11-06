with open('jewellery-design-html/drive_audit_contact_sheet.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Contact sheet size:", len(c))
# count how many img tags are in contact sheet
import re
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', c)
print(f"Total images displayed in contact sheet: {len(imgs)}")
for src in imgs[:15]:
    print(" ", src)


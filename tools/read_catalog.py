import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('jewellery-design-html/js/catalog.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find product blocks
pattern = re.compile(r'id:\s*[\'"]([^\'"]+)[\'"].*?name:\s*[\'"]([^\'"]+)[\'"].*?category:\s*[\'"]([^\'"]+)[\'"].*?price:\s*(\d+).*?mrp:\s*(\d+)', re.DOTALL)
for match in pattern.finditer(text):
    pid, name, cat, price, mrp = match.groups()
    print(f"ID: {pid} | {name} | {cat} | Rs.{price} (MRP Rs.{mrp})")

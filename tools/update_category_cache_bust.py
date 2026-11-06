import re

def update_cache_bust(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Replace v=drive_curated_v1 with v=authentic_products_v2
    new_text = re.sub(r'(\.webp|\.jpg|\.png)\?v=[a-zA-Z0-9_\-]+', r'\1?v=authentic_products_v2', text)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"Updated cache busters in {file_path}")

update_cache_bust('jewellery-design-html/categories.html')
update_cache_bust('jewellery-design-html/index.html')

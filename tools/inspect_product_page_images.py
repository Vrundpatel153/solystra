from bs4 import BeautifulSoup
import re

print("=== Analyzing product.html ===")
with open('jewellery-design-html/product.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

images = soup.find_all('img')
print(f"Total img tags in product.html: {len(images)}")

seen_sections = set()
for img in images:
    src = img.get('src', '')
    alt = img.get('alt', '')
    parent = img.parent
    grandparent = parent.parent if parent else None
    
    # get classes
    img_cls = img.get('class', [])
    parent_cls = parent.get('class', []) if parent else []
    gp_cls = grandparent.get('class', []) if grandparent else []
    
    # check for aspect ratio in img or parent or grandparent
    aspect = None
    for item in [img, parent, grandparent]:
        if item:
            classes = ' '.join(item.get('class', []))
            m = re.search(r'aspect-[a-zA-Z0-9\-\/\[\]]+', classes)
            if m:
                aspect = m.group(0)
                break
    
    # determine section
    section_name = "Other"
    p_str = str(parent) + str(grandparent)
    if 'gallery' in p_str.lower() or 'main-image' in p_str.lower() or 'product-image' in p_str.lower():
        section_name = "Main Product Gallery"
    elif 'thumb' in p_str.lower():
        section_name = "Gallery Thumbnails"
    elif 'pairing' in p_str.lower() or 'bundle' in p_str.lower() or 'complete' in p_str.lower():
        section_name = "Pairing / Complete the Look"
    elif 'related' in p_str.lower() or 'like' in p_str.lower() or 'grid' in p_str.lower():
        section_name = "Related Products / You May Also Like"
    elif 'review' in p_str.lower():
        section_name = "Reviews / UGC"
    elif 'packaging' in p_str.lower() or 'box' in p_str.lower():
        section_name = "Packaging / Gift Box"
    elif 'cert' in p_str.lower() or 'hallmark' in p_str.lower():
        section_name = "Authenticity / Certificate"
    
    key = (section_name, aspect, ' '.join(parent_cls)[:50])
    if key not in seen_sections:
        seen_sections.add(key)
        print(f"\n[Section: {section_name}]")
        print(f"  Image src: {src[:60]}")
        print(f"  Image alt: {alt}")
        print(f"  Parent class: {' '.join(parent_cls)}")
        print(f"  Aspect ratio class: {aspect}")


def adjust_spacing():
    path = 'jewellery-design-html/products.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update Title from "Curated Handcrafted Collection" to "Curated Collection"
    html = html.replace('Curated Handcrafted Collection</span>', 'Curated Collection</span>')
    
    # Update Sort button min-width and padding
    html = html.replace('min-w-[130px]', 'min-w-[118px]')
    html = html.replace('px-3.5 py-1.5 min-w-[145px]', 'px-2.5 py-1.5 min-w-[118px]')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Adjusted spacing in products.html")

if __name__ == '__main__':
    adjust_spacing()


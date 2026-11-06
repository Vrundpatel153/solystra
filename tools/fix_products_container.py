import re

def fix_products_container():
    path = 'jewellery-design-html/products.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the mobile control stack end and the extra closing div
    # Look for the string right before id="products-catalog-grid"
    pos_grid = html.find('id="products-catalog-grid"')
    if pos_grid == -1:
        print("ERROR: could not find products-catalog-grid")
        return

    snippet_before = html[max(0, pos_grid-120):pos_grid]
    print("Snippet before grid:", repr(snippet_before))

    # Look for multiple </div> right before <div id="products-catalog-grid"
    # We saw \n</div></div><div or \n</div>\n</div><div
    # Let's clean it so mobile stack closes its own divs, and products-catalog-grid is directly inside <main class="w-full">
    pattern = r'(</div>\s*</div>\s*</div>\s*</div>)\s*</div>\s*(<div[^>]*id="products-catalog-grid")'
    m = re.search(pattern, html)
    if m:
        print("Found extra closing div before grid! Replacing...")
        html = html[:m.start()] + m.group(1) + '\n\n' + m.group(2) + html[m.end():]
    else:
        # Check if there is another pattern
        print("Could not match regex, inspecting exact ending...")
        # Let's inspect the mobile controls container:
        mob_start = html.find('<!-- Mobile Control Stack')
        # Let's count open/close divs inside mobile control stack
        mob_end = pos_grid
        mob_code = html[mob_start:mob_end]
        opens = mob_code.count('<div')
        closes = mob_code.count('</div')
        print(f"Inside mobile control stack: opens={opens}, closes={closes}")
        if closes > opens:
            excess = closes - opens
            print(f"Excess closing divs: {excess}")
            # Remove the excess </div> at the end of mob_code
            last_div_idx = mob_code.rfind('</div>')
            new_mob_code = mob_code[:last_div_idx] + mob_code[last_div_idx+len('</div>'):]
            html = html[:mob_start] + new_mob_code + html[mob_end:]
            print("Removed excess closing div!")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("products.html container updated.")

if __name__ == '__main__':
    fix_products_container()

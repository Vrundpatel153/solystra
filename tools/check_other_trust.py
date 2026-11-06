for fpath in ['jewellery-design-html/offers.html', 'jewellery-design-html/product.html']:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    idx = c.find('7-Day Exchanges')
    if idx != -1:
        s = c.rfind('<section', 0, idx)
        if s == -1:
            s = c.rfind('<div class="grid grid-cols-4', 0, idx)
        e = c.find('1-Year Warranty', idx)
        e = c.find('</div>', e) + len('</div>')
        print(f"\n=== {fpath} ===")
        print(c[s:s+300])

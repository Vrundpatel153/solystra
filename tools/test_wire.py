import re

with open('jewellery-design-html/categories.html', 'r', encoding='utf-8') as f:
    html = f.read()

category_map = [
    ('Bracelets &amp; Kadas', 'bracelets'),
    ('Bracelets & Kadas', 'bracelets'),
    ('Necklaces &amp; Pendants', 'necklaces'),
    ('Necklaces & Pendants', 'necklaces'),
    ('Rings &amp; Bands', 'rings'),
    ('Rings & Bands', 'rings'),
    ('Earrings &amp; Studs', 'earrings'),
    ('Earrings & Studs', 'earrings'),
    ('Gift Suites &amp; Sets', 'complete_sets'),
    ('Gift Suites & Sets', 'complete_sets'),
    ('Classic Layering Chains', 'chains'),
    ('Anklets &amp; Payals', 'anklets'),
    ('Anklets & Payals', 'anklets'),
    ('Sacred Mangalsutras', 'mangalsutras'),
    ('Solitaire Nose Pins', 'nose_pins'),
    ("Men's Silver Collection", 'mens'),
    ("Men&#39;s Silver Collection", 'mens')
]

print("Script template ready.")


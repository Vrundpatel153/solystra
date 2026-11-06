import os

css_addition = """

/* Solystra Atelier Split-Editorial Hero Slider */
.solystra-hero-wrap {
  position: relative !important;
  width: 100% !important;
  height: 520px !important;
  background-color: #141210 !important;
  overflow: hidden !important;
}

@media (min-width: 640px) {
  .solystra-hero-wrap {
    height: 480px !important;
  }
}

@media (min-width: 1024px) {
  .solystra-hero-wrap {
    height: 520px !important;
  }
}
"""

css_paths = [
    'jewellery-design-html/css/styles.css',
    'jewellery-design-html-dist/css/styles.css',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\css\styles.css',
    'public/css/styles.css'
]

for p in css_paths:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        if '.solystra-hero-wrap' not in c:
            with open(p, 'a', encoding='utf-8') as f:
                f.write(css_addition)
            print(f"Added .solystra-hero-wrap to {p}")
        else:
            print(f"Already exists in {p}")

# Now update index.html in jewellery-design-html and targets
index_paths = [
    'jewellery-design-html/index.html',
    'jewellery-design-html-dist/index.html',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\index.html'
]

for ip in index_paths:
    if os.path.exists(ip):
        with open(ip, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the inner div of hero
        target_str = '<div class="relative w-full h-[520px] sm:h-[480px] lg:h-[520px]">'
        replacement = '<div class="solystra-hero-wrap">'
        if target_str in content:
            content = content.replace(target_str, replacement)
            with open(ip, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {ip} with .solystra-hero-wrap")
        else:
            print(f"Target string not found in {ip}")

print("Permanent hero CSS applied!")

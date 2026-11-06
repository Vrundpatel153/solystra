import os

css_addition = """

/* Solystra Split Editorial Pure Flexbox Classes */
.solystra-hero-desktop-grid {
  display: none;
  width: 100%;
  height: 100%;
}

@media (min-width: 640px) {
  .solystra-hero-desktop-grid {
    display: flex !important;
    flex-direction: row !important;
  }
}

.solystra-hero-card {
  width: 45% !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  padding: 2rem 2.5rem !important;
  background-color: #161412 !important;
  border-right: 1px solid rgba(44, 39, 35, 0.6) !important;
  position: relative !important;
  z-index: 10 !important;
  flex-shrink: 0 !important;
}

@media (min-width: 1024px) {
  .solystra-hero-card {
    padding: 3rem 4rem !important;
    width: 42% !important;
  }
}

.solystra-hero-img-col {
  width: 55% !important;
  height: 100% !important;
  position: relative !important;
  overflow: hidden !important;
  background-color: #000 !important;
  flex-grow: 1 !important;
}

@media (min-width: 1024px) {
  .solystra-hero-img-col {
    width: 58% !important;
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
        with open(p, 'a', encoding='utf-8') as f:
            f.write(css_addition)
        print(f"Appended flexbox CSS to {p}")

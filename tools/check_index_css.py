import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/index.css', 'r', encoding='utf-8') as f:
    text = f.read()

if '.pdp-fixed-gallery' in text:
    print(".pdp-fixed-gallery found in src/index.css")
else:
    print(".pdp-fixed-gallery NOT found in src/index.css, adding it...")
    addition = """
/* Fixed Left Product Gallery on Desktop - Only right side scrolls */
@media (min-width: 1024px) {
  .pdp-fixed-gallery {
    position: -webkit-sticky !important;
    position: sticky !important;
    top: calc(74px + 1.5rem) !important;
    align-self: flex-start !important;
  }
}
"""
    with open('src/index.css', 'a', encoding='utf-8') as f:
        f.write(addition)
    print("Added .pdp-fixed-gallery to src/index.css")


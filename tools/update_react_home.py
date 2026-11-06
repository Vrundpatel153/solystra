import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('src/pages/HomePage.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('const HERO_BANNERS = [')
idx2 = text.find('];', idx) + 2

new_banners = """const HERO_BANNERS = [
  {
    id: 1,
    desktopImg: 'solystra_assets/banners/hero_model_1_pc.webp?v=model2026',
    mobileImg: 'solystra_assets/banners/hero_model_1_mob.webp?v=model2026',
    title: 'The Solitaire Heart Suite',
    subtitle: 'Pure 925 sterling silver with brilliant Austrian solitaire heart pendant.',
    desc: 'Crafted in pure 925 sterling silver with a sparkling Austrian solitaire heart pendant.',
    tag: 'ATELIER SIGNATURE',
    cta: 'Explore Necklaces',
    category: 'necklaces'
  },
  {
    id: 2,
    desktopImg: 'solystra_assets/banners/hero_model_2_pc.webp?v=model2026',
    mobileImg: 'solystra_assets/banners/hero_model_2_mob.webp?v=model2026',
    title: 'Modern Classics Collection',
    subtitle: 'Double-layered solitaire diamond and natural freshwater pearl necklace.',
    desc: 'Tailored luxury chic featuring natural freshwater pearls and brilliant solitaire accents.',
    tag: 'MOST LOVED',
    cta: 'Shop Complete Sets',
    category: 'complete-sets'
  },
  {
    id: 3,
    desktopImg: 'solystra_assets/banners/hero_model_3_pc.webp?v=model2026',
    mobileImg: 'solystra_assets/banners/hero_model_3_mob.webp?v=model2026',
    title: 'Royal Crown Solitaire',
    subtitle: 'Bespoke tiara-cut dancing solitaire in handcrafted 925 sterling silver.',
    desc: 'Finished with dual-micron anti-tarnish rhodium for a lifetime of mirror brilliance.',
    tag: 'NEW ARRIVALS',
    cta: 'View Solitaires',
    category: 'necklaces'
  },
  {
    id: 4,
    desktopImg: 'solystra_assets/banners/hero_model_4_pc.webp?v=model2026',
    mobileImg: 'solystra_assets/banners/hero_model_4_mob.webp?v=model2026',
    title: 'Austrian Tennis Bracelet',
    subtitle: 'Continuous hand-set Austrian solitaires in 18K Italian gold vermeil & 925 silver.',
    desc: 'Continuous hand-set Austrian solitaires in radiant 18K Italian gold vermeil & 925 silver.',
    tag: 'ICONIC SILHOUETTE',
    cta: 'Discover Bracelets',
    category: 'bracelets'
  }
];"""

text = text[:idx] + new_banners + text[idx2:]
with open('src/pages/HomePage.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated src/pages/HomePage.jsx successfully!")

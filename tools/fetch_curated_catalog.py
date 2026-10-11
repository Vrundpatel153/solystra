"""
fetch_curated_catalog.py
Fetches a balanced, multi-category research media pack (photos + HD MP4 videos)
covering all core jewelry types of Zavya:
- Rings (Women's, Solitaire, Couple)
- Necklaces & Pendants (Chains, Mangalsutras, Pendants)
- Bracelets (Kada, Chain, Charm)
- Men's Collection (Rings, Chains, Bracelets)
- Anklets
- Jewellery Sets
- Gift Hampers & Festive Collections
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADER = os.path.join(BASE_DIR, 'tools', 'download_zavya.py')

TARGET_CATEGORIES = [
    ('womens_ring', 4),
    ('diamond_solitaire_ring', 3),
    ('couple_ring', 3),
    ('necklace', 4),
    ('pendant', 4),
    ('diamond_pendant', 3),
    ('mangalsutra', 3),
    ('bracelet', 4),
    ('chain_bracelet', 3),
    ('charm_bracelet', 3),
    ('kada_bracelet', 3),
    ('mens_ring', 3),
    ('men_chain', 3),
    ('men_bracelet', 3),
    ('anklets', 4),
    ('jewellery_sets', 3),
    ('gift_hamper', 4),
    ('valentines', 3)
]

def main():
    print("=== Starting Comprehensive Multi-Category Media Pack Download ===")
    total_cats = len(TARGET_CATEGORIES)
    for idx, (cat, limit) in enumerate(TARGET_CATEGORIES, 1):
        print(f"\n[{idx}/{total_cats}] Processing category '{cat}' (limit: {limit} products, with HD videos)...")
        cmd = [
            sys.executable,
            DOWNLOADER,
            '--category', cat,
            '--limit', str(limit),
            '--videos',
            '--threads', '8'
        ]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"Warning: Category {cat} exited with code {res.returncode}")

    print("\n=== Curated Multi-Category Media Pack Finished Successfully ===")

if __name__ == '__main__':
    main()

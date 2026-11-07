import os

search_terms = ['banner_floral_portrait', 'banner_profile_floral', 'collection_daily_luxe', 'banner_pc_3', 'banner_mob_3']
dirs_to_check = ['jewellery-design-html', 'jewellery-design-html-dist', 'c:/Users/vrund/OneDrive/Desktop/solystra-html']

for d in dirs_to_check:
    if not os.path.exists(d):
        continue
    print(f"\n=== Searching in {d} ===")
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith(('.html', '.js', '.css', '.json')):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                        content = fp.read()
                        for term in search_terms:
                            if term in content:
                                print(f"Found {term} in {fpath}")
                except Exception as e:
                    pass


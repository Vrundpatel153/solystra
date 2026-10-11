import urllib.request
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
BASE_URL = 'https://solystrajewels.com'

# 1. Fetch all products from Shopify
print("1. Fetching all products from solystrajewels.com...")
prod_req = urllib.request.Request(f"{BASE_URL}/products.json?limit=250&page=1", headers=HEADERS)
with urllib.request.urlopen(prod_req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    products = data.get('products', [])

print(f"   Successfully fetched {len(products)} products from solystrajewels.com.")

# 2. Fetch all collections to map category and metal memberships
collections_to_fetch = [
    'bracelets', 'necklaces', 'earrings', 'rings', 
    'silver-anklets', 'complete-sets', 'chains', 'pendant-sets',
    'gold', 'silver', 'blush-tones', 'mens'
]

print("\n2. Fetching collections for precise categorization...")
collections_map = {}
for col in collections_to_fetch:
    url = f"{BASE_URL}/collections/{col}/products.json?limit=250"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            col_data = json.loads(resp.read().decode('utf-8'))
            collections_map[col] = [p['handle'] for p in col_data.get('products', [])]
            print(f"   Collection '{col}': {len(collections_map[col])} products")
        time.sleep(0.2)
    except Exception as e:
        print(f"   Collection '{col}' fetch warning: {e}")
        collections_map[col] = []

# Save raw dump for reference & build_catalog
os.makedirs('src/data', exist_ok=True)
with open('src/data/solystra_shopify_dump.json', 'w', encoding='utf-8') as f:
    json.dump({
        'products': products,
        'collections_map': collections_map,
        'fetched_at': time.time()
    }, f, indent=2, ensure_ascii=False)
print("   Saved master shopify dump to src/data/solystra_shopify_dump.json")

# 3. Download product images concurrently
products_dir = os.path.join('solystra_assets', 'products')
os.makedirs(products_dir, exist_ok=True)

download_tasks = []

for p in products:
    handle = p['handle']
    p_dir = os.path.join(products_dir, handle)
    os.makedirs(p_dir, exist_ok=True)
    
    images = p.get('images', [])
    for idx, img_obj in enumerate(images):
        src_url = img_obj.get('src')
        if not src_url:
            continue
        # Strip query params from url to get clean extension
        clean_url = src_url.split('?')[0]
        ext = os.path.splitext(clean_url)[1].lower()
        if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp']:
            ext = '.png'
            
        file_name = f"angle_{idx + 1}{ext}"
        dest_path = os.path.join(p_dir, file_name)
        
        # Check if already exists and is non-empty (> 5KB)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 5000:
            continue
            
        download_tasks.append((src_url, dest_path, handle))

print(f"\n3. Found {len(download_tasks)} images that need downloading into {products_dir}...")

def download_image(task):
    url, dest, handle = task
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            if len(content) > 1000:
                with open(dest, 'wb') as f:
                    f.write(content)
                return True, dest
            return False, f"Empty content for {dest}"
    except Exception as e:
        return False, f"Error {url} -> {dest}: {e}"

success_count = 0
failed_count = 0

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_image, task) for task in download_tasks]
    for future in as_completed(futures):
        success, res = future.result()
        if success:
            success_count += 1
        else:
            failed_count += 1
            print(f"   [Download Error]: {res}")

print(f"\n   Image download complete: {success_count} succeeded, {failed_count} failed.")

# Summary of local directories
local_dirs = [d for d in os.listdir(products_dir) if os.path.isdir(os.path.join(products_dir, d))]
print(f"Total product folders in {products_dir}: {len(local_dirs)}")

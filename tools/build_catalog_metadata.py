"""
build_catalog_metadata.py
Extracts full catalog metadata for all products from https://www.zavya.co/
Includes product titles, handles, categories, tags, pricing, and all image/video URLs.
Saves to zavya_assets/metadata/catalog_metadata.json
"""

import os
import json
import urllib.request
import urllib.parse
import time
import concurrent.futures

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_DIR = os.path.join(BASE_DIR, 'zavya_assets', 'metadata')
os.makedirs(METADATA_DIR, exist_ok=True)

OUTPUT_CATALOG_FILE = os.path.join(METADATA_DIR, 'catalog_metadata.json')
OUTPUT_SUMMARY_FILE = os.path.join(METADATA_DIR, 'catalog_summary.json')

def fetch_page(page_num, limit=250):
    url = f"https://www.zavya.co/products.json?page={page_num}&limit={limit}"
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                products = data.get('products', [])
                print(f"Page {page_num}: fetched {len(products)} products")
                return products
        except Exception as e:
            print(f"Page {page_num} attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return []

def fetch_product_media(handle):
    """Fetches full media array (including 1080p MP4 videos) from product .js endpoint"""
    url = f"https://www.zavya.co/products/{handle}.js"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            media_list = []
            for m in data.get('media', []):
                mtype = m.get('media_type')
                if mtype == 'video':
                    sources = m.get('sources', [])
                    # Pick highest resolution MP4
                    mp4s = [s for s in sources if s.get('mime_type') == 'video/mp4']
                    mp4s.sort(key=lambda s: s.get('height', 0), reverse=True)
                    video_url = mp4s[0]['url'] if mp4s else (sources[0]['url'] if sources else None)
                    preview = m.get('preview_image', {}).get('src')
                    media_list.append({
                        'type': 'video',
                        'url': video_url,
                        'preview': preview,
                        'duration': m.get('duration')
                    })
                elif mtype == 'image':
                    src = m.get('src')
                    if src:
                        media_list.append({
                            'type': 'image',
                            'url': src
                        })
            return handle, media_list
    except Exception:
        return handle, []

def main():
    print("=== Building Complete Zavya Product Catalog Metadata ===")
    all_products = []
    page = 1

    while True:
        products = fetch_page(page, limit=250)
        if not products:
            break
        all_products.extend(products)
        page += 1
        time.sleep(0.5)

    print(f"\nTotal raw products fetched: {len(all_products)}")

    # Standardize and catalog items
    categories = {}
    catalog = []

    for p in all_products:
        pid = p.get('id')
        title = p.get('title')
        handle = p.get('handle')
        ptype = (p.get('product_type') or 'Uncategorized').strip()
        tags = p.get('tags') or []
        vendor = p.get('vendor')
        created_at = p.get('created_at')
        variants = p.get('variants', [])
        
        price = variants[0].get('price') if variants else None
        compare_price = variants[0].get('compare_at_price') if variants else None
        sku = variants[0].get('sku') if variants else None

        raw_images = p.get('images', [])
        image_urls = []
        for img in raw_images:
            src = img.get('src')
            if src:
                # Remove crop/resize params for full resolution
                clean_src = src.split('?')[0]
                image_urls.append({
                    'id': img.get('id'),
                    'url': clean_src,
                    'alt': img.get('alt'),
                    'width': img.get('width'),
                    'height': img.get('height')
                })

        item = {
            'id': pid,
            'title': title,
            'handle': handle,
            'category': ptype,
            'sku': sku,
            'price': price,
            'compare_at_price': compare_price,
            'tags': tags,
            'created_at': created_at,
            'image_count': len(image_urls),
            'images': image_urls,
            'videos': []  # Populated for selected samples or on demand
        }

        catalog.append(item)
        categories[ptype] = categories.get(ptype, 0) + 1

    print("\n--- Product Categories Breakdown ---")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:30}: {count} products")

    # Sample top products in each category to discover video media
    print("\nScanning sample products across categories for video media...")
    sample_handles = []
    seen_cats = set()
    for item in catalog:
        cat = item['category']
        if cat not in seen_cats and len(sample_handles) < 60:
            sample_handles.append(item['handle'])
            seen_cats.add(cat)
        elif sample_handles.count(cat) < 3 and len(sample_handles) < 60:
            sample_handles.append(item['handle'])

    videos_found_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_product_media, h): h for h in sample_handles}
        for future in concurrent.futures.as_completed(futures):
            handle, media_list = future.result()
            videos = [m for m in media_list if m['type'] == 'video']
            if videos:
                videos_found_count += len(videos)
                # Attach to catalog item
                for item in catalog:
                    if item['handle'] == handle:
                        item['videos'] = videos
                        break

    print(f"Discovered {videos_found_count} videos among sampled products.")

    # Save complete metadata
    with open(OUTPUT_CATALOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)

    total_images = sum(item['image_count'] for item in catalog)
    summary = {
        'total_products': len(catalog),
        'total_images': total_images,
        'average_images_per_product': round(total_images / len(catalog), 2) if catalog else 0,
        'categories': categories,
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(OUTPUT_SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\nSuccessfully wrote catalog metadata: {OUTPUT_CATALOG_FILE}")
    print(f"Successfully wrote summary: {OUTPUT_SUMMARY_FILE}")
    print(f"Total products cataloged: {len(catalog)}")
    print(f"Total images cataloged: {total_images}")

if __name__ == '__main__':
    main()

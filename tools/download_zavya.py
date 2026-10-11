"""
download_zavya.py
Resumable, multithreaded downloader for Zavya product imagery and HD videos.
Supports filtering by category, product limits, images per product, video inclusion,
and disk-space safety guards.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import argparse
import concurrent.futures
import shutil
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(BASE_DIR, 'zavya_assets', 'products')
CATALOG_METADATA_FILE = os.path.join(BASE_DIR, 'zavya_assets', 'metadata', 'catalog_metadata.json')

def get_disk_free_gb(path):
    try:
        total, used, free = shutil.disk_usage(path)
        return free / (1024 ** 3)
    except Exception:
        return 999.0

def sanitize_folder_name(name):
    # Remove characters invalid in Windows/Linux folders
    clean = "".join([c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name])
    clean = clean.strip().replace(' ', '_').lower()
    return clean or 'other'

def download_file(url, dest_path, min_bytes=500):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > min_bytes:
        return {'status': 'skipped', 'size': os.path.getsize(dest_path), 'path': dest_path}

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    temp_path = dest_path + '.tmp'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if len(data) < min_bytes:
                return {'status': 'too_small', 'size': len(data), 'path': dest_path}
            with open(temp_path, 'wb') as f:
                f.write(data)
        if os.path.exists(dest_path):
            os.remove(dest_path)
        os.rename(temp_path, dest_path)
        return {'status': 'downloaded', 'size': len(data), 'path': dest_path}
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return {'status': 'error', 'error': str(e), 'path': dest_path}

def fetch_product_videos(handle):
    """Fetch product .js endpoint to discover 1080p MP4 videos if not in catalog"""
    url = f"https://www.zavya.co/products/{handle}.js"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            videos = []
            for m in data.get('media', []):
                if m.get('media_type') == 'video':
                    sources = m.get('sources', [])
                    mp4s = [s for s in sources if s.get('mime_type') == 'video/mp4']
                    mp4s.sort(key=lambda s: s.get('height', 0), reverse=True)
                    if mp4s:
                        videos.append(mp4s[0]['url'])
            return videos
    except Exception:
        return []

def main():
    parser = argparse.ArgumentParser(description="Zavya Media & Product Downloader")
    parser.add_argument('--category', type=str, default='all', help="Filter by category (e.g. 'rings', 'earrings', 'pendant', 'bracelet', 'mens', 'all')")
    parser.add_argument('--limit', type=int, default=10, help="Max products per category (default: 10, set 0 for all)")
    parser.add_argument('--max-images', type=int, default=0, help="Max images per product (default 0 = all images)")
    parser.add_argument('--videos', action='store_true', help="Include HD 1080p product showcase videos")
    parser.add_argument('--threads', type=int, default=8, help="Concurrent download threads (default 8)")
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR, help="Destination directory")
    parser.add_argument('--min-disk-free-gb', type=float, default=5.0, help="Stop download if disk free space falls below this threshold in GB (safety guard)")
    args = parser.parse_args()

    out_dir = os.path.abspath(args.output_dir)
    os.makedirs(out_dir, exist_ok=True)

    free_gb = get_disk_free_gb(out_dir)
    print(f"Destination folder: {out_dir}")
    print(f"Current disk free space: {free_gb:.2f} GB (Safety threshold: {args.min_disk_free_gb} GB)")

    if free_gb < args.min_disk_free_gb:
        print(f"ERROR: Disk space is below safety cap of {args.min_disk_free_gb} GB! Aborting.")
        sys.exit(1)

    if not os.path.exists(CATALOG_METADATA_FILE):
        print(f"ERROR: Catalog metadata file not found at {CATALOG_METADATA_FILE}. Run tools/build_catalog_metadata.py first.")
        sys.exit(1)

    with open(CATALOG_METADATA_FILE, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"Loaded {len(catalog)} products from catalog metadata.")

    # Filter by category
    cat_filter = args.category.lower().strip()
    grouped_products = {}
    for p in catalog:
        cat = p.get('category') or 'Other'
        norm_cat = sanitize_folder_name(cat)
        if cat_filter != 'all' and cat_filter not in norm_cat and norm_cat not in cat_filter:
            continue
        grouped_products.setdefault(norm_cat, []).append(p)

    selected_products = []
    for norm_cat, prods in sorted(grouped_products.items()):
        limit = args.limit if args.limit > 0 else len(prods)
        chosen = prods[:limit]
        selected_products.extend(chosen)
        print(f"  Category '{norm_cat}': selected {len(chosen)} / {len(prods)} products")

    print(f"\nTotal products queued for download: {len(selected_products)}")

    download_tasks = []
    for prod in selected_products:
        cat_folder = sanitize_folder_name(prod.get('category', 'other'))
        handle = prod.get('handle') or f"prod_{prod.get('id')}"
        prod_dir = os.path.join(out_dir, cat_folder, handle)
        os.makedirs(prod_dir, exist_ok=True)

        # Save product-level json metadata
        meta_path = os.path.join(prod_dir, 'product_info.json')
        if not os.path.exists(meta_path):
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(prod, f, indent=2)

        # Images
        images = prod.get('images', [])
        if args.max_images > 0:
            images = images[:args.max_images]

        for idx, img in enumerate(images, start=1):
            url = img.get('url')
            if not url:
                continue
            ext = os.path.splitext(urllib.parse.urlparse(url).path)[1] or '.jpg'
            img_filename = f"{idx:02d}_{handle}{ext}"
            img_dest = os.path.join(prod_dir, img_filename)
            download_tasks.append({
                'type': 'image',
                'url': url,
                'dest': img_dest,
                'handle': handle
            })

        # Videos
        if args.videos:
            existing_videos = [v.get('url') for v in prod.get('videos', []) if v.get('url')]
            if not existing_videos:
                existing_videos = fetch_product_videos(handle)
            for v_idx, v_url in enumerate(existing_videos, start=1):
                vid_filename = f"video_{v_idx:02d}_{handle}.mp4"
                vid_dest = os.path.join(prod_dir, vid_filename)
                download_tasks.append({
                    'type': 'video',
                    'url': v_url,
                    'dest': vid_dest,
                    'handle': handle
                })

    print(f"Total media items to process: {len(download_tasks)} ({sum(1 for t in download_tasks if t['type']=='image')} images, {sum(1 for t in download_tasks if t['type']=='video')} videos)")

    downloaded = 0
    skipped = 0
    errors = 0
    total_bytes = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_map = {executor.submit(download_file, t['url'], t['dest']): t for t in download_tasks}
        for future in concurrent.futures.as_completed(future_map):
            task = future_map[future]
            try:
                res = future.result()
                status = res.get('status')
                size = res.get('size', 0)
                total_bytes += size
                if status == 'downloaded':
                    downloaded += 1
                    if downloaded % 10 == 0 or task['type'] == 'video':
                        print(f"  [{task['type'].upper()}] {os.path.basename(res['path'])} ({size / (1024*1024):.2f} MB)")
                elif status == 'skipped':
                    skipped += 1
                else:
                    errors += 1
                    print(f"  [ERROR] {task['url']}: {res.get('error')}")
            except Exception as e:
                errors += 1
                print(f"  [EXCEPTION] {task['url']}: {e}")

            # Check disk space periodically
            if (downloaded + skipped) % 50 == 0:
                cur_free = get_disk_free_gb(out_dir)
                if cur_free < args.min_disk_free_gb:
                    print(f"\n[ALERT] Disk space ({cur_free:.2f} GB) reached minimum safe limit ({args.min_disk_free_gb} GB)! Pausing downloads.")
                    break

    print("\n=== Download Complete ===")
    print(f"Downloaded: {downloaded} new files")
    print(f"Skipped (already cached): {skipped} files")
    print(f"Errors: {errors}")
    print(f"Total size: {total_bytes / (1024*1024):.2f} MB ({total_bytes / (1024**3):.3f} GB)")
    print(f"Remaining disk free: {get_disk_free_gb(out_dir):.2f} GB")

if __name__ == '__main__':
    main()

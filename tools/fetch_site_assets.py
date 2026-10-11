"""
fetch_site_assets.py
Fetches all banners, hero imagery, promotional strips, category cards,
and branding assets from https://www.zavya.co/
"""

import os
import re
import urllib.request
import urllib.parse
import json
import concurrent.futures
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_BANNERS_DIR = os.path.join(BASE_DIR, 'zavya_assets', 'site_banners')
BRANDING_DIR = os.path.join(BASE_DIR, 'zavya_assets', 'branding')
METADATA_DIR = os.path.join(BASE_DIR, 'zavya_assets', 'metadata')

os.makedirs(SITE_BANNERS_DIR, exist_ok=True)
os.makedirs(BRANDING_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

TARGET_PAGES = [
    'https://www.zavya.co/',
    'https://www.zavya.co/collections/best-sellers',
    'https://www.zavya.co/collections/new-arrivals',
    'https://www.zavya.co/collections/rings',
    'https://www.zavya.co/collections/earrings',
    'https://www.zavya.co/collections/necklaces-pendants',
    'https://www.zavya.co/collections/bracelets',
    'https://www.zavya.co/pages/about-us'
]

def fetch_page_html(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def clean_url(url):
    if not url:
        return None
    url = url.strip().strip('"\'()')
    if url.startswith('//'):
        url = 'https:' + url
    elif url.startswith('/'):
        url = 'https://www.zavya.co' + url
    elif not url.startswith('http'):
        url = 'https://' + url

    # Remove dynamic sizing query params like _100x100, _compact, etc. to get master original
    clean = url.split('&')[0].split('?')[0]
    # Remove Shopify size suffix like _300x300, _large, etc. before extension if present
    clean = re.sub(r'_(?:\d+x\d*|\d*x\d+|small|compact|medium|large|grande|master|1024x1024|2048x2048)(\.[a-zA-Z0-9]+)$', r'\1', clean)
    return clean

def download_file(item):
    url = item['url']
    dest_path = item['path']
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        return {'url': url, 'status': 'skipped', 'size': os.path.getsize(dest_path), 'path': dest_path}

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) < 100:  # Ignore empty or placeholder responses
                return {'url': url, 'status': 'too_small', 'size': len(data)}
            with open(dest_path, 'wb') as f:
                f.write(data)
            return {'url': url, 'status': 'downloaded', 'size': len(data), 'path': dest_path}
    except Exception as e:
        return {'url': url, 'status': 'error', 'error': str(e)}

def categorize_asset(url, filename):
    lower = (url + ' ' + filename).lower()
    branding_keywords = ['logo', 'icon', 'badge', 'certificate', 'whysilver', 'seal', 'authenticity', 'trust', 'strip']
    if any(k in lower for k in branding_keywords) or filename.endswith('.svg'):
        return os.path.join(BRANDING_DIR, filename), 'branding'
    return os.path.join(SITE_BANNERS_DIR, filename), 'site_banner'

def main():
    print("=== Scanning Zavya.co for Site Banners & Branding Assets ===")
    found_urls = set()

    for page_url in TARGET_PAGES:
        print(f"Crawling: {page_url}")
        html = fetch_page_html(page_url)
        if not html:
            continue

        # Extract Shopify files, cdn files, img tags, background-images
        patterns = [
            r'https?://cdn\.shopify\.com/s/files/[^\s"\'<>\)\,\}]+',
            r'(?:https:)?//www\.zavya\.co/cdn/shop/files/[^\s"\'<>\)\,\}]+',
            r'(?:https:)?//(?:www\.)?zavya\.co/cdn/shop/t/\d+/assets/[^\s"\'<>\)\,\}]+',
            r'(?:src|data-src|data-srcset|poster|content)=["\']([^"\']+\.(?:jpg|jpeg|png|webp|svg|gif|mp4))["\']'
        ]

        for pat in patterns:
            matches = re.findall(pat, html, re.I)
            for m in matches:
                if isinstance(m, tuple):
                    m = m[0]
                cleaned = clean_url(m)
                if cleaned and any(cleaned.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.mp4']):
                    # Ignore common third-party analytics/pixel images
                    if any(bad in cleaned.lower() for bad in ['facebook', 'google', 'pickrr', 'razorpay', 'clarity', 'analytics']):
                        continue
                    found_urls.add(cleaned)

    print(f"\nDiscovered {len(found_urls)} unique site banner and branding media URLs.")

    download_tasks = []
    manifest = []
    seen_filenames = set()

    for url in sorted(found_urls):
        raw_name = os.path.basename(urllib.parse.urlparse(url).path)
        if not raw_name:
            continue
        
        # Ensure unique filename
        filename = raw_name
        counter = 1
        name_part, ext = os.path.splitext(raw_name)
        while filename in seen_filenames:
            filename = f"{name_part}_{counter}{ext}"
            counter += 1
        seen_filenames.add(filename)

        dest_path, category = categorize_asset(url, filename)
        item = {
            'url': url,
            'filename': filename,
            'path': dest_path,
            'category': category
        }
        download_tasks.append(item)
        manifest.append({
            'filename': filename,
            'url': url,
            'category': category,
            'relative_path': os.path.relpath(dest_path, BASE_DIR).replace('\\', '/')
        })

    print(f"Downloading {len(download_tasks)} assets concurrently (threads: 8)...")
    downloaded_count = 0
    skipped_count = 0
    total_bytes = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_file, task): task for task in download_tasks}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res.get('status') == 'downloaded':
                downloaded_count += 1
                total_bytes += res.get('size', 0)
                print(f"  [DOWNLOADED] {os.path.basename(res['path'])} ({res['size']/1024:.1f} KB)")
            elif res.get('status') == 'skipped':
                skipped_count += 1
                total_bytes += res.get('size', 0)
            else:
                print(f"  [FAILED/SKIPPED] {res.get('url')}: {res.get('status')} {res.get('error', '')}")

    manifest_file = os.path.join(METADATA_DIR, 'site_assets_manifest.json')
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print("\n=== Site Asset Download Complete ===")
    print(f"Total processed: {len(download_tasks)}")
    print(f"New downloads: {downloaded_count}")
    print(f"Previously existing: {skipped_count}")
    print(f"Total data size: {total_bytes / (1024*1024):.2f} MB")
    print(f"Saved manifest: {manifest_file}")

if __name__ == '__main__':
    main()

import os
import sys
import json
import urllib.request
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

import yt_dlp

reel_urls = [
    "https://www.instagram.com/reel/DaFwwDoSUFL/",
    "https://www.instagram.com/reel/DaiPSBhyTkV/",
    "https://www.instagram.com/reel/DaVVXNOSQxw/",
    "https://www.instagram.com/reel/DYtkml_yz66/",
    "https://www.instagram.com/reel/DYhd6MnysBj/",
    "https://www.instagram.com/reel/DZXkay2y6VU/",
    "https://www.instagram.com/reel/DavF6Jlyvwd/",
    "https://www.instagram.com/reel/DegrYkoKQrI/"
]

output_dir = 'jewellery-design-html/solystra_assets/videos'
poster_dir = 'jewellery-design-html/solystra_assets/videos/posters'
os.makedirs(output_dir, exist_ok=True)
os.makedirs(poster_dir, exist_ok=True)

ydl_opts = {
    'quiet': True,
    'no_warnings': True,
}

reels_data = []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for idx, url in enumerate(reel_urls, 1):
        reel_code = url.split('/reel/')[1].split('/')[0]
        print(f"[{idx}/8] Processing {reel_code}...")
        try:
            info = ydl.extract_info(url, download=False)
            title = info.get('title') or f"Solystra Reel {idx}"
            desc = info.get('description') or ""
            video_url = info.get('url')
            thumbnail = info.get('thumbnail')
            
            # Target file paths
            video_filename = f"reel_{idx:02d}_{reel_code}.mp4"
            poster_filename = f"poster_{idx:02d}_{reel_code}.webp"
            jpg_poster = f"poster_{idx:02d}_{reel_code}.jpg"
            
            video_path = os.path.join(output_dir, video_filename)
            poster_path = os.path.join(poster_dir, poster_filename)
            temp_jpg = os.path.join(poster_dir, jpg_poster)
            
            # Download video
            if video_url:
                print(f"  Downloading video -> {video_filename}")
                urllib.request.urlretrieve(video_url, video_path)
            
            # Download and convert thumbnail
            if thumbnail:
                print(f"  Downloading poster -> {poster_filename}")
                urllib.request.urlretrieve(thumbnail, temp_jpg)
                try:
                    im = Image.open(temp_jpg)
                    im.save(poster_path, 'WEBP', quality=88)
                    if os.path.exists(temp_jpg):
                        os.remove(temp_jpg)
                except Exception as e:
                    print(f"  Error converting poster: {e}")
            
            first_line = desc.strip().split('\n')[0] if desc else f"Atelier Reel {idx}"
            if len(first_line) > 50:
                first_line = first_line[:47] + "..."
            
            reels_data.append({
                "index": idx,
                "code": reel_code,
                "url": url,
                "desc": desc,
                "first_line": first_line,
                "video_file": f"solystra_assets/videos/{video_filename}",
                "poster_file": f"solystra_assets/videos/posters/{poster_filename}",
                "video_size": os.path.getsize(video_path) if os.path.exists(video_path) else 0,
                "poster_size": os.path.getsize(poster_path) if os.path.exists(poster_path) else 0
            })
            print(f"  Done: Video size: {reels_data[-1]['video_size']} bytes, Poster: {reels_data[-1]['poster_size']} bytes")
        except Exception as err:
            print(f"  Failed to process {url}: {err}")

with open('tools/reels_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(reels_data, f, indent=2, ensure_ascii=False)

print("\n--- Summary ---")
print(f"Downloaded {len(reels_data)} / {len(reel_urls)} reels successfully!")

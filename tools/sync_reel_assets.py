import os
import shutil

src_videos = 'jewellery-design-html/solystra_assets/videos'
src_posters = 'jewellery-design-html/solystra_assets/videos/posters'

target_bases = [
    'jewellery-design-html-dist/solystra_assets/videos',
    r'c:\Users\vrund\OneDrive\Desktop\solystra-html\solystra_assets\videos',
    'solystra_assets/videos',
    'public/solystra_assets/videos',
    'dist/solystra_assets/videos'
]

reel_files = [f for f in os.listdir(src_videos) if f.startswith('reel_0') and f.endswith('.mp4')]
poster_files = [f for f in os.listdir(src_posters) if f.startswith('poster_0') and f.endswith('.webp')]

print(f"Syncing {len(reel_files)} videos and {len(poster_files)} posters...")

for base in target_bases:
    os.makedirs(base, exist_ok=True)
    os.makedirs(os.path.join(base, 'posters'), exist_ok=True)
    
    for vf in reel_files:
        src = os.path.join(src_videos, vf)
        dst = os.path.join(base, vf)
        shutil.copy2(src, dst)
        
    for pf in poster_files:
        src = os.path.join(src_posters, pf)
        dst = os.path.join(base, 'posters', pf)
        shutil.copy2(src, dst)
        
    print(f"Synced to {base}")

print("All reel assets synced successfully!")


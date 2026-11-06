import urllib.request
import re

url = 'https://drive.google.com/drive/folders/11uGB087Uruph7Xj9M_JEybPUL5Z4lqW0'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Drive folder HTTP response length: {len(html)}")
        
        # Look for file IDs and names in the raw JS payload
        matches = re.findall(r'\["([a-zA-Z0-9_-]{25,})","([^"]+?\.(?:jpg|jpeg|png|webp|JPG|JPEG|PNG))"', html)
        print(f"Extracted direct regex matches: {len(matches)}")
        for fid, fname in matches[:20]:
            print(f"  {fname} -> {fid}")
            
        # Also look for subfolders
        folder_matches = re.findall(r'\["([a-zA-Z0-9_-]{25,})","([^"]+?)","application/vnd\.google-apps\.folder"', html)
        print(f"Subfolders found: {len(folder_matches)}")
        for fid, fname in folder_matches:
            print(f"  FOLDER: {fname} -> {fid}")

except Exception as e:
    print(f"Error accessing Drive: {e}")


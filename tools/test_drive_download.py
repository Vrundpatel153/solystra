import urllib.request
import os

fid = "1THuTyuXnHkpR28WJkOr7uLUJNuSOmtQg" # banner-1-pc.png
urls_to_test = [
    f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t",
    f"https://lh3.googleusercontent.com/u/0/d/{fid}=w2560",
    f"https://lh3.googleusercontent.com/u/0/d/{fid}",
    f"https://docs.google.com/uc?export=download&id={fid}"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for u in urls_to_test:
    print(f"\nTesting URL: {u}")
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content_type = resp.headers.get('Content-Type')
            content_len = resp.headers.get('Content-Length')
            data = resp.read()
            print(f"Status: {resp.status}, Content-Type: {content_type}, Size: {len(data)} bytes, Header Length: {content_len}")
            if len(data) > 10000:
                print("SUCCESSFUL IMAGE DOWNLOAD!")
                with open("scratch/test_banner_1_pc.png", "wb") as f:
                    f.write(data)
                break
    except Exception as e:
        print("Error:", e)

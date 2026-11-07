import asyncio
import json
import urllib.request
import websockets
import re

FOLDERS = {
    "categories": "121UWtzFAtkHSv2Xgi6iRi9nTGdBIiMrZ",
    "collections": "1k4H06CKQrAi_yMisrQzD9HCnsZNYgNnY",
    "hero-banner": "1g8Z-yT3VIm8VD9eXm0uXMtCEtT-sDm3y"
}

async def scrape_folder(ws, folder_name, folder_id):
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    print(f"\n--- Navigating to {folder_name} ({url}) ---")
    msg_id = 100
    
    async def send(method, params=None):
        nonlocal msg_id
        m = {"id": msg_id, "method": method, "params": params or {}}
        msg_id += 1
        await ws.send(json.dumps(m))
        while True:
            res = json.loads(await ws.recv())
            if res.get("id") == m["id"]:
                return res.get("result", {})

    await send("Page.navigate", {"url": url})
    await asyncio.sleep(5)

    script_data = await send("Runtime.evaluate", {
        "expression": """(() => {
            const scripts = Array.from(document.querySelectorAll('script'));
            for (const s of scripts) {
                if (s.className && s.className.startsWith('ds:3')) {
                    return s.textContent;
                }
            }
            return document.body.innerHTML;
        })()""",
        "returnByValue": True
    })
    raw_text = script_data.get('result', {}).get('value', '')
    
    with open(f"scratch/folder_{folder_name}_raw.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)

    # In Google Drive ds:3 data, items follow:
    # [[null,"FILE_ID"],null,null,null,"MIME_TYPE", ... [[["FILE_NAME",null,1]]]
    # Let's extract pairs of (file_id, file_name)
    items = []
    # Find all file IDs and names in the text
    # Pattern: [null,"([a-zA-Z0-9_-]{25,40})"].*?\[\[\["([^"]+)"
    pattern = r'\[(?:null,)?\"([a-zA-Z0-9_-]{25,40})\"\](?:(?!\[null,\").)*?\[\[\[\"([^\"]+)\"'
    matches = re.findall(pattern, raw_text, re.DOTALL)
    seen_ids = set()
    for fid, fname in matches:
        if fid != folder_id and fid not in seen_ids:
            seen_ids.add(fid)
            items.append({"id": fid, "name": fname})
            print(f"  -> Found File: {fname} (ID: {fid})")

    # If regex missed any, let's also do a broader regex
    if not items:
        # Fallback: find all strings ending in .png, .jpg, .jpeg, .webp
        file_matches = re.findall(r'\"([a-zA-Z0-9_-]{25,40})\".*?\"([^\"]+\.(?:png|jpg|jpeg|webp|JPG|PNG))\"', raw_text)
        for fid, fname in file_matches:
            if fid not in seen_ids:
                seen_ids.add(fid)
                items.append({"id": fid, "name": fname})
                print(f"  -> Fallback File: {fname} (ID: {fid})")

    return items

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    
    tab = None
    for t in tabs:
        if t.get('type') == 'page' and 'drive.google.com' in t.get('url', ''):
            tab = t
            break
            
    if not tab:
        print("Drive tab not found")
        return

    ws_url = tab['webSocketDebuggerUrl']
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            m = {"id": msg_id, "method": method, "params": params or {}}
            msg_id += 1
            await ws.send(json.dumps(m))
            while True:
                res = json.loads(await ws.recv())
                if res.get("id") == m["id"]:
                    return res.get("result", {})

        await send("Page.enable")
        
        all_results = {}
        for folder_name, folder_id in FOLDERS.items():
            files = await scrape_folder(ws, folder_name, folder_id)
            all_results[folder_name] = files

        with open("scratch/all_drive_subfolders.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2)
        print("\nAll folder files saved to scratch/all_drive_subfolders.json!")

if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import json
import urllib.request
import websockets

async def parse_601_items():
    req = urllib.request.Request("http://127.0.0.1:9222/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    
    drive_tab = next((t for t in tabs if 'drive.google.com' in t.get('url', '')), None)
    if not drive_tab:
        print("No drive tab found")
        return
        
    async with websockets.connect(drive_tab['webSocketDebuggerUrl'], max_size=50*1024*1024) as ws:
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

        # Extract all elements that have data-id and non-empty aria-label or text
        res = await send("Runtime.evaluate", {
            "expression": """
                (() => {
                    const map = {};
                    document.querySelectorAll('div[data-id]').forEach(d => {
                        const id = d.getAttribute('data-id');
                        const label = d.getAttribute('aria-label') || d.innerText || '';
                        if (id && id.length > 20 && id !== '11uGB087Uruph7Xj9M_JEybPUL5Z4lqW0') {
                            if (!map[id] || (label && label.length > map[id].length)) {
                                map[id] = label.trim();
                            }
                        }
                    });
                    return map;
                })()
            """,
            "returnByValue": True
        })
        
        items = res.get('result', {}).get('value', {})
        print(f"Total unique IDs extracted: {len(items)}")
        
        # Save to scratch/drive_all_600_mapped.json
        with open('scratch/drive_all_600_mapped.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=2)
            
        # Analysis
        jpgs = {}
        arws = {}
        folders = {}
        others = {}
        for fid, name in items.items():
            u = name.upper()
            if '.JPG' in u or '.JPEG' in u:
                jpgs[fid] = name
            elif '.ARW' in u:
                arws[fid] = name
            elif 'FOLDER' in u or 'RAW' in u:
                folders[fid] = name
            else:
                others[fid] = name
                
        print(f"JPGs: {len(jpgs)}")
        print(f"ARWs: {len(arws)}")
        print(f"Folders: {len(folders)}")
        print(f"Others/Blank labels: {len(others)}")
        
        print("\nSample JPGs:")
        for fid, name in list(jpgs.items())[:10]:
            print(f"  {name} -> {fid}")
            
        print("\nFolders:")
        for fid, name in folders.items():
            print(f"  {name} -> {fid}")

asyncio.run(parse_601_items())


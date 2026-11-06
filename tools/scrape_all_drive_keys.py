import asyncio
import json
import urllib.request
import websockets

async def get_all():
    url = "https://drive.google.com/drive/folders/11uGB087Uruph7Xj9M_JEybPUL5Z4lqW0"
    req = urllib.request.Request(f"http://127.0.0.1:9222/json/new?{url}", method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
    
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
        await asyncio.sleep(4)
        
        # 1. Find all subfolders first
        folders_res = await send("Runtime.evaluate", {
            "expression": """
                (() => {
                    const folders = [];
                    document.querySelectorAll('[data-id]').forEach(el => {
                        const label = el.getAttribute('aria-label') || el.innerText || '';
                        const id = el.getAttribute('data-id');
                        if (label.toLowerCase().includes('folder') || el.querySelector('[data-mime-type*="folder"]')) {
                            folders.push({id, label});
                        }
                    });
                    return folders;
                })()
            """,
            "returnByValue": True
        })
        print("Subfolders found:", folders_res.get('result', {}).get('value'))
        
        # Click on the main file list area to focus it
        await send("Runtime.evaluate", {
            "expression": """
                const item = document.querySelector('[data-id]');
                if (item) item.focus();
            """
        })
        
        all_items = {}
        
        # Scroll continuously using PageDown keys
        for step in range(40):
            # Read current visible items
            res = await send("Runtime.evaluate", {
                "expression": """
                    (() => {
                        const found = [];
                        document.querySelectorAll('[data-id]').forEach(el => {
                            const id = el.getAttribute('data-id');
                            const label = el.getAttribute('aria-label') || '';
                            const text = el.innerText || '';
                            if (id && id.length > 20) {
                                found.push({id, label: label || text});
                            }
                        });
                        return found;
                    })()
                """,
                "returnByValue": True
            })
            
            items = res.get('result', {}).get('value', [])
            for item in items:
                all_items[item['id']] = item['label']
                
            # Press PageDown
            await send("Input.dispatchKeyEvent", {
                "type": "keyDown",
                "windowsVirtualKeyCode": 34, # PageDown
                "nativeVirtualKeyCode": 34
            })
            await send("Input.dispatchKeyEvent", {
                "type": "keyUp",
                "windowsVirtualKeyCode": 34,
                "nativeVirtualKeyCode": 34
            })
            await asyncio.sleep(0.5)
            
            if (step + 1) % 5 == 0:
                print(f"Step {step+1}: Accumulated {len(all_items)} unique items so far...")

        print(f"\nTOTAL UNIQUE ITEMS ACCUMULATED: {len(all_items)}")
        
        # Save to scratch/all_drive_items_600.json
        with open('scratch/all_drive_items_600.json', 'w', encoding='utf-8') as f:
            json.dump(all_items, f, indent=2)
            
        # Group by file extension
        exts = {}
        for fid, name in all_items.items():
            ext = name.split('.')[-1].upper() if '.' in name else 'NO_EXT'
            exts[ext] = exts.get(ext, 0) + 1
        print("Extension counts:", exts)

asyncio.run(get_all())

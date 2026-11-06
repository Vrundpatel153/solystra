import asyncio
import json
import urllib.request
import websockets
import time

async def inspect_drive():
    url = "https://drive.google.com/drive/folders/11uGB087Uruph7Xj9M_JEybPUL5Z4lqW0"
    print("Opening Google Drive URL in Chrome...")
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
        # wait 4s for Drive to load
        print("Waiting for Drive page to load...")
        await asyncio.sleep(5)
        
        # Check title and content
        title_res = await send("Runtime.evaluate", {"expression": "document.title"})
        print("Page title:", title_res.get('result', {}).get('value'))
        
        # Check current items count
        count_res = await send("Runtime.evaluate", {
            "expression": "document.querySelectorAll('[data-id]').length"
        })
        print("Initial [data-id] count:", count_res.get('result', {}).get('value'))
        
        # Scroll down multiple times to trigger virtual list loading
        for i in range(15):
            await send("Runtime.evaluate", {
                "expression": """
                    const scroller = document.querySelector('[role="main"]') || document.querySelector('.c-P-V') || window;
                    if (scroller.scrollBy) {
                        scroller.scrollBy(0, 3000);
                    } else {
                        window.scrollBy(0, 3000);
                    }
                """
            })
            await asyncio.sleep(1)
            
            c = await send("Runtime.evaluate", {
                "expression": "document.querySelectorAll('[data-id]').length"
            })
            print(f"Scroll {i+1}: [data-id] count = {c.get('result', {}).get('value')}")
            
        # Also extract all labels and data-ids
        extract_res = await send("Runtime.evaluate", {
            "expression": """
                (() => {
                    const items = {};
                    document.querySelectorAll('[data-id]').forEach(el => {
                        const id = el.getAttribute('data-id');
                        const label = el.getAttribute('aria-label') || el.innerText || '';
                        if (id && id.length > 20) {
                            items[id] = label;
                        }
                    });
                    return {
                        count: Object.keys(items).length,
                        sample: Object.entries(items).slice(0, 20)
                    };
                })()
            """,
            "returnByValue": True
        })
        print("Extracted items:", extract_res.get('result', {}).get('value'))

asyncio.run(inspect_drive())

